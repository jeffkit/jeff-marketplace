# Nano-PPT Plugin

AI-powered PPT presentation creator using Google's Gemini image generation model (nano-banana).

## Overview

The Nano-PPT plugin enables Claude Code to create professional PowerPoint presentations through a structured, four-phase workflow:

1. **Requirements Gathering** - Understanding user needs through conversational interview
2. **Brief Outline** - Creating high-level slide structure and narrative flow
3. **Detailed Outline** - Expanding to complete content and visual specifications
4. **Slide Generation** - Generating individual slides as images using Google Gemini

## Features

- 🎨 **AI-Powered Slide Design** - Leverages Google's Gemini 2.5 Flash Image model
- 🔄 **Visual Consistency** - Maintains coherent style across all slides using reference images
- 📊 **Structured Workflow** - Guided process from requirements to final slides
- ✅ **User Approval Gates** - Review and approve at each phase
- 🎯 **Structured Workflow** - Phased approach from requirements to final slides
- 🌐 **Bilingual Support** - Works in English and Chinese

## Installation

### 1. Install the Plugin

Copy this directory to your Claude Code plugins folder:

```bash
cp -r nano-ppt ~/.claude/plugins/
```

### 2. Install Python Dependencies

```bash
cd ~/.claude/plugins/nano-ppt
pip install -r requirements.txt
```

Or install packages directly:

```bash
pip install google-genai Pillow
```

### 3. Set Up API Key

Get your Google AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey), then:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

To make it permanent, add to your shell profile:

```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## Usage

### Triggering the Skill

The skill activates when you request presentation creation:

**English**:
- "Create a PowerPoint presentation about..."
- "Make a slide deck for..."
- "Help me build a presentation on..."
- "I need slides for..."

**Chinese**:
- "帮我创建一个PPT关于..."
- "制作演示文稿..."
- "做个presentation..."

### Example Session

```
User: 帮我创建一个关于Q4营销成果的PPT

Claude: I'll help you create a PPT presentation about Q4 marketing results.
Let me start by gathering your requirements.

[Requirements gathering conversation...]

Claude: Based on our discussion, I understand you want:
- 12 slides covering Q4 marketing performance
- Professional corporate style
- Data-driven with key metrics
- Target audience: Executive team

Is this correct?

User: Yes, that's right.

Claude: Great! I'll create a brief outline showing the slide structure.

[Brief outline presented...]

Claude: Does this structure and flow make sense?

User: Perfect!

Claude: Excellent! Now I'll create the detailed outline with complete content
and visual specifications.

[Detailed outline presented...]

Claude: Please review. Is everything accurate?

User: Yes, let's generate the slides.

Claude: I'll generate the slides now. This will take a few minutes...

✓ Slide 1/12 generated: Title & Key Highlights
✓ Slide 2/12 generated: Executive Summary
...
✓ Slide 12/12 generated: Next Quarter Priorities

All done! Your presentation is ready in ./ppt-output/q4-marketing-results/
```

## Workflow Phases

### Phase 1: Requirements Gathering

The main skill agent conducts a conversational interview to understand:
- Presentation topic and purpose
- Target audience
- Content requirements
- Style and visual preferences
- Technical specifications

**Output**: `requirements.json` saved to `./ppt-output/[name]/`

### Phase 2: Brief Outline

The main skill agent creates:
- Slide titles and main ideas
- Transition relationships between slides
- Overall narrative flow

**Output**: `brief-outline.md` saved to `./ppt-output/[name]/`

### Phase 3: Detailed Outline

The main skill agent expands to:
- Complete content specifications
- Visual requirements and layout
- Design consistency guidelines
- Production notes

**Output**: `detailed-outline.md` saved to `./ppt-output/[name]/`

### Phase 4: Slide Generation

The main skill agent generates each slide:
- Creates images using Google Gemini
- Maintains visual consistency via reference images
- Follows detailed specifications
- Generates sequentially for coherence

**Output**: PNG images for each slide

## Plugin Structure

```
nano-ppt/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── skills/
│   └── nano-ppt/
│       ├── SKILL.md                 # Main skill (all phases)
│       └── scripts/
│           ├── slide_generator.py   # Python script for image generation
│           └── export_slides.py     # Export to PPTX/PDF
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

> **Note**: All phases (1-4) are executed directly by the main skill agent. No sub-agents are used.

## Configuration

### Image Resolution

Output image resolution (requires `gemini-3-pro-image-preview` model):
- `1K` - 1024x1024 pixels
- `2K` - 2048x2048 pixels (default)
- `4K` - 4096x4096 pixels

> **Note**: Must use uppercase 'K' (e.g., `2K` not `2k`).

### Aspect Ratios

Default is 16:9, but you can specify:
- `1:1` - Square
- `2:3`, `3:2` - Portrait/Landscape
- `3:4`, `4:3` - Standard
- `4:5`, `5:4` - Photo
- `9:16`, `16:9` - Widescreen (default)
- `21:9` - Ultra-wide

### Output Directory

Generated slides are saved to:
```
./ppt-output/[presentation-name]/
```

Customize by specifying output path in generation phase.

### Environment Variables

- `GEMINI_API_KEY` - **Required** - Your Google AI API key

## Limitations

1. **Output Format**: Slides are generated as PNG images, not editable .pptx files
2. **Style Variation**: Some visual inconsistency may occur despite reference images
3. **Generation Time**: Each slide takes 10-30 seconds
4. **API Costs**: Each slide generation consumes API quota
5. **Text Rendering**: Complex typography may not always render perfectly

## Troubleshooting

### Missing API Key

```bash
# Check if set
echo $GEMINI_API_KEY

# Set it
export GEMINI_API_KEY="your-key-here"
```

### Import Errors

```bash
pip install --upgrade google-genai Pillow
```

### Visual Inconsistency

- Ensure reference images are being passed correctly
- Make style requirements more specific in detailed outline
- Add explicit consistency instructions

### Generation Failures

- Check API quota and rate limits
- Simplify visual requirements
- Verify prompt isn't too long
- Review error messages carefully

## Version History

### v1.0.0 (Initial Release)
- Four-phase workflow (requirements → brief → detailed → generation)
- Google Gemini integration for image generation
- Visual consistency via reference images
- Structured phased workflow
- Bilingual support (English/Chinese)

## Credits

Created by jeffkit for the jeff-marketplace plugin collection.

## License

This plugin is part of the jeff-marketplace repository.
