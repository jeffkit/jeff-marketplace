#!/usr/bin/env python3
"""
Slide Generator for nano-ppt plugin
Generates PPT slides using Google's Gemini image generation model
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List

# Try importing required packages, handle import errors gracefully
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def install_dependencies():
    """Install required Python dependencies"""
    required_packages = {
        'google-genai': False,
        'Pillow': False
    }

    # Check current availability
    try:
        from google import genai
        from google.genai import types
        required_packages['google-genai'] = True
    except ImportError:
        pass

    try:
        from PIL import Image
        required_packages['Pillow'] = True
    except ImportError:
        pass

    all_installed = True

    for package, is_installed in required_packages.items():
        if is_installed:
            print(f"✅ {package} is already installed")
        else:
            print(f"⚠️  {package} not found, installing automatically...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                all_installed = False

    return all_installed


class SlideGenerator:
    """Generates presentation slides using Google Gemini image model"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the slide generator

        Args:
            api_key: Google GenAI API key (defaults to GEMINI_API_KEY env var)
        """
        # Ensure dependencies are available
        self._ensure_dependencies()

        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable or api_key parameter is required")

        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-3-pro-image-preview"

    def _ensure_dependencies(self):
        """Ensure required dependencies are available, install if needed"""
        if not GENAI_AVAILABLE or not PIL_AVAILABLE:
            print("🔍 Missing dependencies detected, installing automatically...")
            if not install_dependencies():
                raise RuntimeError("Failed to install required dependencies. Please install manually: pip install google-genai Pillow")

    def generate_slide(
        self,
        prompt: str,
        output_path: str,
        aspect_ratio: str = "16:9",
        reference_image: Optional[str] = None,
        reference_images: Optional[List[str]] = None,
        template: Optional[str] = None,
        template_config: Optional[Dict[str, Any]] = None,
        page_type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a single slide image

        Args:
            prompt: Text description of the slide content
            output_path: Path to save the generated image
            aspect_ratio: Image aspect ratio (default: 16:9)
            reference_image: Optional path to single reference image (legacy support)
            reference_images: Optional list of paths to reference images (brand refs, etc.)
            template: Optional path to template image for this page type
            template_config: Optional template configuration dict
            page_type: Optional page type (cover, section, content, data, closing)
            context: Optional context information (ppt overview, previous slide info, etc.)

        Returns:
            Path to the generated image
        """
        # Build enhanced prompt with context and template info
        enhanced_prompt = self._build_prompt(prompt, context, template_config, page_type)

        # Prepare contents for generation
        contents = []
        style_instructions = []

        # Priority 1: Template image (strongest style anchor)
        if template and os.path.exists(template):
            template_img = Image.open(template)
            contents.append(template_img)
            page_type_str = page_type or "slide"
            style_instructions.append(f"Use this template as the base layout for a {page_type_str} slide.")

        # Priority 2: Multiple reference images (brand refs)
        if reference_images:
            for img_path in reference_images:
                if os.path.exists(img_path):
                    ref_img = Image.open(img_path)
                    contents.append(ref_img)
            if len([p for p in reference_images if os.path.exists(p)]) > 0:
                style_instructions.append("Draw visual style inspiration from the reference images.")

        # Priority 3: Single reference image (previous slide - legacy support)
        if reference_image and os.path.exists(reference_image):
            ref_img = Image.open(reference_image)
            contents.append(ref_img)
            style_instructions.append("Maintain visual consistency with the reference slide.")

        # Build style instruction prefix
        if style_instructions:
            style_prefix = " ".join(style_instructions) + " "
            contents.insert(0, style_prefix)

        # Add the main prompt
        contents.append(enhanced_prompt)

        # Generate image
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                    ),
                ),
            )

            # Save generated image
            for part in response.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    image.save(output_path)
                    return output_path
                elif part.text is not None:
                    print(f"Model response text: {part.text}", file=sys.stderr)

            raise RuntimeError("No image generated in response")

        except Exception as e:
            raise RuntimeError(f"Failed to generate slide: {str(e)}")

    def _build_prompt(
        self,
        base_prompt: str,
        context: Optional[Dict[str, Any]] = None,
        template_config: Optional[Dict[str, Any]] = None,
        page_type: Optional[str] = None
    ) -> str:
        """
        Build enhanced prompt with context and template information

        Args:
            base_prompt: Base slide description
            context: Context information including:
                - ppt_overview: Overall PPT theme and structure
                - slide_title: Current slide title
                - slide_main_idea: Main idea to convey
                - previous_slide: Previous slide info for continuity
                - next_slide: Next slide info for flow
                - style_requirements: Specific style requirements
            template_config: Template configuration with brand info
            page_type: Type of page (cover, section, content, etc.)

        Returns:
            Enhanced prompt string
        """
        if not context and not template_config:
            return f"Create a professional presentation slide: {base_prompt}"

        prompt_parts = []

        # Add page type context if available
        if page_type:
            prompt_parts.append(f"Create a professional {page_type.upper()} slide for a presentation.")
        else:
            prompt_parts.append("Create a professional presentation slide.")
        prompt_parts.append("")

        # Add template/brand configuration if available
        if template_config:
            brand_info = template_config.get('brand_info', {})
            if brand_info:
                if brand_info.get('primary_color'):
                    prompt_parts.append(f"Primary Color: {brand_info['primary_color']}")
                if brand_info.get('secondary_color'):
                    prompt_parts.append(f"Secondary Color: {brand_info['secondary_color']}")
                if brand_info.get('accent_color'):
                    prompt_parts.append(f"Accent Color: {brand_info['accent_color']}")
                if brand_info.get('font_heading'):
                    prompt_parts.append(f"Heading Font Style: {brand_info['font_heading']}")
                prompt_parts.append("")

            # Add page-type specific layout hints
            page_types = template_config.get('page_types', {})
            if page_type and page_type in page_types:
                page_config = page_types[page_type]
                elements = page_config.get('elements', {})
                if elements:
                    prompt_parts.append("Layout Requirements:")
                    for elem_name, elem_config in elements.items():
                        if isinstance(elem_config, dict) and elem_config.get('position'):
                            prompt_parts.append(f"  - {elem_name}: {elem_config.get('position')}")
                    prompt_parts.append("")

        prompt_parts.append("Requirements:")

        # Add PPT overview context
        if context and context.get('ppt_overview'):
            prompt_parts.append(f"Presentation Theme: {context['ppt_overview']}")
            prompt_parts.append("")

        # Add current slide information
        if context and context.get('slide_title'):
            prompt_parts.append(f"Slide Title: {context['slide_title']}")

        if context and context.get('slide_main_idea'):
            prompt_parts.append(f"Main Idea: {context['slide_main_idea']}")

        prompt_parts.append(f"Content: {base_prompt}")
        prompt_parts.append("")

        # Add continuity context
        if context and context.get('previous_slide'):
            prompt_parts.append(f"Previous Slide Context (for visual continuity): {context['previous_slide']}")

        if context and context.get('next_slide'):
            prompt_parts.append(f"Next Slide Preview (for narrative flow): {context['next_slide']}")

        # Add style requirements
        if context and context.get('style_requirements'):
            prompt_parts.append("")
            prompt_parts.append(f"Style Requirements: {context['style_requirements']}")

        return "\n".join(prompt_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Generate PPT slides using Google Gemini image model"
    )
    parser.add_argument(
        "prompt",
        nargs='?',  # Make prompt optional
        help="Text description of the slide content"
    )
    parser.add_argument(
        "output",
        nargs='?',  # Make output optional
        help="Output image path"
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check and install required dependencies (google-genai, Pillow)"
    )
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        choices=["16:9", "9:16", "4:3", "3:4", "1:1"],
        help="Slide aspect ratio (default: 16:9)"
    )
    parser.add_argument(
        "--reference-image",
        help="Path to single reference image for style consistency (legacy)"
    )
    parser.add_argument(
        "--reference-images",
        nargs='+',
        help="Paths to multiple reference images (brand refs, style samples)"
    )
    parser.add_argument(
        "--template",
        help="Path to template image for this page type"
    )
    parser.add_argument(
        "--template-config",
        help="Path to template configuration JSON file"
    )
    parser.add_argument(
        "--page-type",
        choices=["cover", "section", "content", "data", "visual", "closing"],
        help="Type of page being generated"
    )
    parser.add_argument(
        "--context",
        help="JSON string or file path containing context information"
    )
    parser.add_argument(
        "--api-key",
        help="Google GenAI API key (or use GEMINI_API_KEY env var)"
    )

    args = parser.parse_args()

    # Handle dependency check mode
    if args.check_deps:
        print("🔍 Checking Python dependencies for nano-ppt...")
        success = install_dependencies()
        if success:
            print("🎉 All dependencies are ready!")
        else:
            print("❌ Some dependencies could not be installed. Please install manually:")
            print("pip install google-genai Pillow")
        sys.exit(0 if success else 1)

    # Validate required arguments for slide generation
    if not args.prompt or not args.output:
        parser.error("prompt and output are required for slide generation")

    # Parse context if provided
    context = None
    if args.context:
        if os.path.isfile(args.context):
            with open(args.context, 'r') as f:
                context = json.load(f)
        else:
            try:
                context = json.loads(args.context)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON context: {args.context}", file=sys.stderr)
                sys.exit(1)

    # Parse template config if provided
    template_config = None
    if args.template_config:
        if os.path.isfile(args.template_config):
            with open(args.template_config, 'r') as f:
                template_config = json.load(f)
        else:
            print(f"Error: Template config file not found: {args.template_config}", file=sys.stderr)
            sys.exit(1)

    # Generate slide
    try:
        generator = SlideGenerator(api_key=args.api_key)
        output_path = generator.generate_slide(
            prompt=args.prompt,
            output_path=args.output,
            aspect_ratio=args.aspect_ratio,
            reference_image=args.reference_image,
            reference_images=args.reference_images,
            template=args.template,
            template_config=template_config,
            page_type=args.page_type,
            context=context
        )
        print(f"Slide generated successfully: {output_path}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
