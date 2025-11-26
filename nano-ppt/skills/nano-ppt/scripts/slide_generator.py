#!/usr/bin/env python3
"""
Slide Generator for nano-ppt plugin
Generates PPT slides using Google's Gemini image generation model
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
from google import genai
from google.genai import types
from PIL import Image


class SlideGenerator:
    """Generates presentation slides using Google Gemini image model"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the slide generator

        Args:
            api_key: Google GenAI API key (defaults to GEMINI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable or api_key parameter is required")

        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash-image"

    def generate_slide(
        self,
        prompt: str,
        output_path: str,
        aspect_ratio: str = "16:9",
        reference_image: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a single slide image

        Args:
            prompt: Text description of the slide content
            output_path: Path to save the generated image
            aspect_ratio: Image aspect ratio (default: 16:9)
            reference_image: Optional path to reference image for style consistency
            context: Optional context information (ppt overview, previous slide info, etc.)

        Returns:
            Path to the generated image
        """
        # Build enhanced prompt with context
        enhanced_prompt = self._build_prompt(prompt, context)

        # Prepare contents for generation
        contents = [enhanced_prompt]

        # Add reference image if provided for style consistency
        if reference_image and os.path.exists(reference_image):
            ref_img = Image.open(reference_image)
            contents.append(ref_img)
            # Add instruction to maintain visual consistency
            contents.insert(0, "Maintain the same visual style, color scheme, and design aesthetic as the reference image. ")

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

    def _build_prompt(self, base_prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Build enhanced prompt with context information

        Args:
            base_prompt: Base slide description
            context: Context information including:
                - ppt_overview: Overall PPT theme and structure
                - slide_title: Current slide title
                - slide_main_idea: Main idea to convey
                - previous_slide: Previous slide info for continuity
                - next_slide: Next slide info for flow
                - style_requirements: Specific style requirements

        Returns:
            Enhanced prompt string
        """
        if not context:
            return f"Create a professional presentation slide: {base_prompt}"

        prompt_parts = [
            "Create a professional presentation slide with the following requirements:",
            ""
        ]

        # Add PPT overview context
        if context.get('ppt_overview'):
            prompt_parts.append(f"Presentation Theme: {context['ppt_overview']}")
            prompt_parts.append("")

        # Add current slide information
        if context.get('slide_title'):
            prompt_parts.append(f"Slide Title: {context['slide_title']}")

        if context.get('slide_main_idea'):
            prompt_parts.append(f"Main Idea: {context['slide_main_idea']}")

        prompt_parts.append(f"Content: {base_prompt}")
        prompt_parts.append("")

        # Add continuity context
        if context.get('previous_slide'):
            prompt_parts.append(f"Previous Slide Context (for visual continuity): {context['previous_slide']}")

        if context.get('next_slide'):
            prompt_parts.append(f"Next Slide Preview (for narrative flow): {context['next_slide']}")

        # Add style requirements
        if context.get('style_requirements'):
            prompt_parts.append("")
            prompt_parts.append(f"Style Requirements: {context['style_requirements']}")

        return "\n".join(prompt_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Generate PPT slides using Google Gemini image model"
    )
    parser.add_argument(
        "prompt",
        help="Text description of the slide content"
    )
    parser.add_argument(
        "output",
        help="Output image path"
    )
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        choices=["16:9", "9:16", "4:3", "3:4", "1:1"],
        help="Slide aspect ratio (default: 16:9)"
    )
    parser.add_argument(
        "--reference-image",
        help="Path to reference image for style consistency"
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

    # Generate slide
    try:
        generator = SlideGenerator(api_key=args.api_key)
        output_path = generator.generate_slide(
            prompt=args.prompt,
            output_path=args.output,
            aspect_ratio=args.aspect_ratio,
            reference_image=args.reference_image,
            context=context
        )
        print(f"Slide generated successfully: {output_path}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
