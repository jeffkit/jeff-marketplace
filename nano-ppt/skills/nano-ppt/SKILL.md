---
name: nano-ppt
description: AI-powered PPT presentation creation using Google's Gemini image generation (nano-banana). Use this skill when users want to create PowerPoint presentations, slides, or visual presentations. Triggers include requests like "创建PPT", "制作演示文稿", "帮我做个presentation", "make a slide deck", or any request to create presentation slides. The skill orchestrates the entire workflow from requirements gathering through slide generation.
---

# Nano-PPT: AI-Powered Presentation Creator

This skill creates professional PPT presentations using Google's Gemini image generation model (gemini-3-pro-image-preview, also known as "nano-banana"). It orchestrates the complete workflow from understanding user requirements to generating individual slides as images.

## Prerequisites

### Required Environment Variables

```bash
export GEMINI_API_KEY="your-google-genai-api-key"
```

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### Required Python Packages

```bash
pip install google-genai Pillow
```

## Workflow Overview

The skill follows a structured, phased approach:

**Phase 0: Template Preparation** → **Phase 1: Requirements Gathering** → **Phase 2: Brief Outline** → **Phase 3: Detailed Outline** → **Phase 4: Slide Generation** → **Phase 5: Incremental Updates** (optional) → **Phase 6: Export** (optional)

- **Phase 0**: Detect or create templates for visual consistency
- **Phases 1-3**: You execute directly, gathering user feedback and iterating in real-time
- **Phase 4**: Delegate to sub-agents for parallel/sequential image generation
- **Phase 5**: Handle post-generation modifications (append, insert, replace slides)
- **Phase 6**: Export to PPTX or PDF format for distribution

## Your Role

You are both the **designer** and **orchestrator**:

**Phase 0 (Template Setup)**:
1. **Check for user templates** - Detect `./ppt-templates/` directory
2. **Offer template options** - Preset, brand-generated, or skip
3. **Prepare visual anchors** - Copy templates to output directory

**Phases 1-3 (Design)**:
1. **Gather requirements** - Interview user conversationally
2. **Create outlines** - Draft brief and detailed outlines yourself
3. **Iterate with user** - Get immediate feedback, make adjustments
4. **Save artifacts** - Write all intermediate files to disk for user review/editing

**Phase 4 (Generation)**:
1. **Delegate to sub-agents** - Use Task tool for slide generation
2. **Track progress** - Report status after each slide
3. **Handle errors** - Retry failed generations with adjusted parameters

## Detailed Workflow

### Phase 0: Template Preparation

**Objective**: Establish visual anchors for consistent slide generation.

**Four Template Paths**:

#### Path A: User-Provided Templates (Auto-detect)

Check if user has prepared templates in `./ppt-templates/`:

```bash
ls ./ppt-templates/
```

**If directory exists with template images:**
1. List found templates and confirm with user:
   "I found existing templates in ./ppt-templates/:
   - cover.png ✓
   - section.png ✓
   - content.png ✓
   - closing.png ✗ (missing)
   
   Should I use these templates? For missing types, I can generate them or use alternatives."

2. If user confirms, copy to `./ppt-output/[name]/templates/`

**Template Directory Structure**:
```
./ppt-templates/           # User places templates here
├── cover.png             # Cover slide template [Required]
├── section.png           # Section divider template [Recommended]
├── content.png           # Content page template [Required]
├── data.png              # Data/chart slide template [Optional]
└── closing.png           # Closing slide template [Recommended]
```

#### Path B: Preset Templates

If no user templates, offer preset options:
```
"Which template style would you like to use?"
1. business-blue - Professional, clean blue theme
2. tech-modern - Gradient tech aesthetic
3. minimal-white - Minimalist with lots of whitespace
4. warm-corporate - Warm tones, approachable feel
```

#### Path C: Generate from Brand Reference

If user wants custom templates:
1. Ask: "Do you have brand reference images? (logo, existing slides, style samples)"
2. Collect image paths and save to `./ppt-output/[name]/brand-refs/`
3. Generate 4 template samples: cover, section, content, closing
4. Present for user approval
5. Iterate if needed

#### Path D: Skip Templates (Gemini Free-form)

If user chooses to skip:
1. Mark presentation as "no-template mode"
2. Slide 1 will be generated purely from text description
3. Subsequent slides use previous slide as reference
4. Note: Style consistency depends entirely on prompts

**Save template choice to requirements**:
```json
{
  "template_mode": "user-provided" | "preset" | "brand-generated" | "none",
  "template_name": "business-blue",  // if preset
  "templates_path": "./ppt-output/[name]/templates/"
}
```

**Proceed to Phase 1** after template setup is complete.

### Phase 1: Requirements Gathering

**Objective**: Understand what presentation the user wants to create.

**Process** (you execute this yourself):

1. **Conduct conversational interview** with the user about:
   - **Presentation Overview**: Target audience, goal, delivery context, tone
   - **Content Requirements**: Key topics, technical depth, comparisons needed, main message
   - **Style Requirements**: Visual style, colors, aspect ratio, branding
   - **Structural Requirements**: Slide count, must-have slide types, organization

2. **Ask one category at a time** - Don't overwhelm with too many questions

3. **Create requirements.json** with this structure:
   ```json
   {
     "presentation_name": "kebab-case-name",
     "overview": {
       "title": "Presentation Title",
       "target_audience": "description",
       "primary_goal": "description",
       "delivery_context": "description",
       "tone": "description"
     },
     "content_requirements": {
       "key_topics": ["topic1", "topic2"],
       "technical_specs": "level of detail needed",
       "comparisons": "if any",
       "call_to_action": "main takeaway"
     },
     "style_requirements": {
       "visual_style": "description",
       "color_preferences": "description",
       "aspect_ratio": "16:9",
       "branding": "guidelines if any"
     },
     "structural_requirements": {
       "slide_count": 5,
       "must_have_slides": ["type1", "type2"],
       "organization_notes": "preferences"
     }
   }
   ```

4. **Save to disk**: `./ppt-output/[presentation-name]/requirements.json`

5. **Confirm with user**: Present summary and get approval

**Quality checks**:
- All fields populated and specific?
- User confirmed requirements?

**Proceed to Phase 2** only after user approval.

### Phase 2: Brief Outline Creation

**Objective**: Create a high-level outline showing slide titles, main ideas, and transitions.

**Process** (you execute this yourself):

1. **Draft the brief outline** in markdown format with:
   - **Presentation Overview**: Topic, audience, key message, total slides, narrative style
   - **Slide Structure**: For each slide:
     - Slide number and title
     - Main idea (2-3 sentences)
     - Transition relationship to previous/next slides
   - **Narrative Flow Summary**: Overall story arc

2. **Example structure**:
   ```markdown
   # [Presentation Title]

   ## Presentation Overview
   - **Topic**: ...
   - **Target Audience**: ...
   - **Key Message**: ...
   - **Total Slides**: N
   - **Narrative Style**: ...
   - **Template Mode**: user-provided | preset | brand-generated | none

   ## Slide Structure

   ### Slide 1: [Title]
   **Page Type**: COVER
   **Main Idea**: ...
   **Transition**: Opening slide, sets the tone...

   ### Slide 2: [Title]
   **Page Type**: SECTION
   **Main Idea**: ...
   **Transition**: Introduces first major topic...

   ### Slide 3: [Title]
   **Page Type**: CONTENT
   **Main Idea**: ...
   **Transition**: Builds on previous slide...

   ...

   ## Narrative Flow Summary
   [2-3 paragraphs describing the overall story arc]
   ```

**Page Types**:
- `COVER` - Opening/title slide
- `SECTION` - Chapter/section divider
- `CONTENT` - Standard content slide
- `DATA` - Chart/graph focused slide
- `VISUAL` - Image-heavy slide
- `CLOSING` - Final/thank you slide

3. **Save to disk**: `./ppt-output/[presentation-name]/brief-outline.md`

4. **Present to user** and ask for feedback:
   - "Does this structure and flow make sense?"
   - "Should any slides be added, removed, or reordered?"

5. **Iterate**: Update the file based on feedback and save again

**Quality checks**:
- Logical flow and structure?
- Appropriate slide count?
- Clear transitions?
- Matches requirements?

**Proceed to Phase 3** only after user approval.

### Phase 3: Detailed Outline Creation

**Objective**: Expand the brief outline into production-ready specifications with complete content and visual requirements for each slide.

**Process** (you execute this yourself):

1. **Create detailed specifications** for each slide in markdown format:

   For each slide, include:
   - **Content Specifications**: Exact text, data points, messages
   - **Visual Specifications**: Layout type, subject, style, composition, specific elements
   - **Color Emphasis**: Primary and accent colors
   - **Typography Notes**: Font sizes, weights, effects
   - **Design Notes**: Intent, mood, key visual goals
   - **Transition Context**: How it connects to previous/next slides

2. **Add production notes** at the end:
   - **Overall Design Consistency**: Cross-slide continuity strategy
   - **Color Palette**: Specific hex codes and usage rules
   - **Typography Guidelines**: Font hierarchy and effects
   - **Image Generation Strategy**: How to maintain style consistency

3. **Example structure**:
   ```markdown
   # [Presentation Title] - Detailed Outline

   ## Presentation Specifications
   [Topic, audience, slides, aspect ratio, visual style, colors]

   ---

   ## Slide 1: [Title]

   ### Content Specifications
   - **Slide Title**: "..."
   - **Subtitle**: "..."
   - **Text Content**: ...

   ### Visual Specifications
   - **Layout Type**: ...
   - **Subject**: ...
   - **Style**: ...
   - **Composition**: ...
   - **Specific Elements**: ...
   - **Color Emphasis**: ...
   - **Typography Notes**: ...

   ### Design Notes
   [Intent, mood, visual goals]

   ### Transition Context
   - **Previous Slide**: N/A (first slide)
   - **Next Slide**: [Preview]
   - **Narrative Connection**: ...

   ---

   [Repeat for each slide]

   ---

   ## Production Notes

   ### Overall Design Consistency
   [Continuity strategy]

   ### Color Palette
   - Primary: #HEX
   - Secondary: #HEX
   - Accent: #HEX

   ### Typography Guidelines
   [Font hierarchy]

   ### Image Generation Strategy
   [Style consistency approach]
   ```

4. **Save to disk**: `./ppt-output/[presentation-name]/detailed-outline.md`

5. **Present to user** and ask:
   - "Is all content accurate and complete?"
   - "Does the visual direction match your expectations?"

6. **Iterate**: Update based on feedback and save again

**Quality checks**:
- Every slide fully specified?
- Visual requirements actionable?
- Consistency strategy defined?
- Aligns with brief outline?

**Proceed to Phase 4** only after user approval.

### Phase 4: Slide Generation

**Objective**: Generate each slide as an image file using Google's Gemini model.

**Setup**:
1. Verify output directory exists: `./ppt-output/[presentation-name]/`
2. Check `GEMINI_API_KEY` environment variable is set
3. Read the detailed outline from disk
4. Check template mode from requirements (templates available in `./ppt-output/[name]/templates/`)

**Note**: The slide generation script automatically handles dependency checking and installation when needed. No manual setup required.

**Process** (delegate to sub-agent):

For each slide in the detailed outline, invoke the sub-agent **sequentially**:

```
Use Task tool with:
- subagent_type: "nano-ppt:nanoppt-slide-generator"
- prompt: Read and follow the instructions in agents/nanoppt-slide-generator.md.
  Generate Slide [N] of [Total].

  Page Type: [COVER | SECTION | CONTENT | DATA | VISUAL | CLOSING]

  Template Info (if using templates):
  - Template Mode: [user-provided | preset | brand-generated | none]
  - Template Image: ./ppt-output/[name]/templates/[page-type].png
  - Template Config: ./ppt-output/[name]/templates/template-config.json

  Presentation Context:
  - Topic: [from requirements]
  - Visual Style: [from requirements]
  - Color Scheme: [from requirements]
  - Aspect Ratio: [from requirements]

  Previous Slide Summary:
  - Slide [N-1]: [brief description and image path]
  - Image path: ./ppt-output/[name]/slides/slide_[N-1].png

  Slide [N] Specifications:
  [Paste the complete slide specifications from detailed-outline.md]

  Output Path: ./ppt-output/[presentation-name]/slides/slide_[NN].png

  Reference Images:
  - Template: ./ppt-output/[name]/templates/[page-type].png (if available)
  - Previous Slide: ./ppt-output/[name]/slides/slide_[N-1].png (if not first slide)

  Generate this slide and report the result.
```

**Key points**:
- Generate slides **in order** (1, 2, 3, ..., N) for style consistency
- Pass page-type template as primary visual anchor
- Each slide (except first) also uses previous slide as reference
- Report progress after each: "✓ Slide [N]/[Total] generated: [title]"
- If generation fails, retry with adjusted parameters

**Final output**:
- Slide images: `./ppt-output/[presentation-name]/slide_01.png`, `slide_02.png`, etc.
- Requirements: `./ppt-output/[presentation-name]/requirements.json`
- Brief outline: `./ppt-output/[presentation-name]/brief-outline.md`
- Detailed outline: `./ppt-output/[presentation-name]/detailed-outline.md`

**Quality checks**:
- All slides generated?
- Visual consistency maintained?
- Content matches specs?

---

### Phase 5: Incremental Updates (Optional)

**Objective**: Modify existing presentations by adding, inserting, or replacing slides.

**Trigger**: User requests changes to an already-generated presentation.

#### 5.1 Requirements Gathering

**Agent asks clarifying questions**:

1. **What type of change?**
   - Add new content
   - Modify existing slide
   - Reorganize/move slides

2. **What is the content?**
   - What topic/information should the new slide cover?
   - What's the main message?

3. **Where should it go?** (if adding)
   - After Slide X (insert)
   - At the end (append)
   - Replace Slide X (replacement)

#### 5.2 Draft New Slide Outline

**Agent creates outline for user approval**:

```markdown
## New Slide: [Title]

**Operation**: Insert after Slide 5 (becomes new Slide 6)

### Brief Outline
- **Page Type**: CONTENT
- **Main Idea**: [2-3 sentences]
- **Transition from Previous**: [connection to Slide 5]
- **Transition to Next**: [connection to current Slide 6]

### Detailed Specification
**Content Specifications**:
- Slide Title: ...
- Text Content: ...

**Visual Specifications**:
- Layout: ...
- Style: Match existing slides
- Reference: Use slide_05.png for style consistency
```

#### 5.3 User Confirmation

Present draft to user and wait for:
- Approval to proceed
- Requests for adjustments
- Cancellation

**Only proceed after explicit user confirmation.**

#### 5.4 Determine Operation Type

Agent automatically determines operation based on user input:

| User Request | Operation Type | File Handling |
|--------------|----------------|---------------|
| "Add at the end" | **APPEND** | Create slide_N+1.png |
| "Add after Slide X" | **INSERT** | Rename X+1~end, then create new X+1 |
| "Replace Slide X" | **REPLACE** | Delete old, regenerate slide_X.png |
| "Modify Slide X content" | **REPLACE** | Same as replace |

#### 5.5 Execute Update

**For APPEND operation**:
1. Update `detailed-outline.md` - add new slide at end
2. Generate new slide using last slide as reference:
   ```bash
   python3 scripts/slide_generator.py \
     "[prompt]" \
     "./slides/slide_16.png" \
     --reference-image "./slides/slide_15.png" \
     --page-type [type]
   ```

**For INSERT operation**:
1. Update `detailed-outline.md` - insert new slide spec at position
2. Rename existing files (shift forward):
   ```bash
   # Example: Insert after Slide 5
   # Move slide_06.png → slide_07.png, etc.
   for i in $(seq [TOTAL] -1 [INSERT_POS+1]); do
     mv slides/slide_$(printf "%02d" $i).png \
        slides/slide_$(printf "%02d" $((i+1))).png
   done
   ```
3. Generate new slide using previous slide as reference
4. **Optional**: Regenerate next slide if transition context changed significantly

**For REPLACE operation**:
1. Update `detailed-outline.md` - modify existing slide spec
2. **Backup or keep old slide as reference** (default behavior for style consistency)
3. Regenerate slide using:
   - **Default**: Old slide (`slide_N.png.bak` or in-memory) as primary reference
   - **Optional**: User can specify `--no-reference` to generate fresh style
   - Also use previous slide (`slide_N-1.png`) for context continuity
4. Delete backup after successful generation
5. **Optional**: Regenerate next slide if content changed significantly

> **Note**: Using old slide as reference ensures the new slide maintains the same visual template. User can explicitly request fresh generation if they want a different look.

#### 5.6 Post-Update Verification

- Confirm new/updated slide generated
- Check file naming is sequential
- Verify style consistency with neighbors
- Report completion to user

**Example interaction**:
```
User: "我想在 Slide 5 之后加一张关于技术债务的内容"

Agent: "好的，我来为您起草这张新幻灯片的内容：

## 新增幻灯片草案

**插入位置**: Slide 5 之后 (成为新的 Slide 6)
**Page Type**: CONTENT
**标题**: 技术债务的隐性成本
**主要内容**: ...

请确认这个内容，或告诉我需要调整的地方。"

User: "确认"

Agent: [执行 INSERT 操作]
"✓ 已在 Slide 5 后插入新幻灯片
 - 原 Slide 6-15 已重命名为 Slide 7-16
 - 新 Slide 6 已生成: slide_06.png"
```

---

### Phase 6: Export (Optional)

**Objective**: Convert generated slide images to shareable formats (PPTX, PDF).

**Available Formats**:
- **PPTX** - Editable PowerPoint format (recommended for further editing)
- **PDF** - Static document format (recommended for distribution)

#### 6.1 Export to PPTX

```bash
python3 scripts/export_slides.py \
  "./ppt-output/[presentation-name]/slides" \
  --format pptx \
  --aspect-ratio "16:9"
```

**Output**: `./ppt-output/[presentation-name]/[presentation-name].pptx`

#### 6.2 Export to PDF

```bash
python3 scripts/export_slides.py \
  "./ppt-output/[presentation-name]/slides" \
  --format pdf
```

**Output**: `./ppt-output/[presentation-name]/[presentation-name].pdf`

#### 6.3 Export to Both Formats

```bash
python3 scripts/export_slides.py \
  "./ppt-output/[presentation-name]/slides" \
  --format both
```

#### 6.4 Custom Output Path

```bash
python3 scripts/export_slides.py \
  "./ppt-output/agent-skills-intro/slides" \
  "./output/my-presentation.pptx" \
  --format pptx
```

#### 6.5 Dependencies

First-time setup:
```bash
python3 scripts/export_slides.py --check-deps
```

Required packages: `python-pptx`, `Pillow`, `img2pdf`

## Error Handling

### Common Issues and Solutions

**Missing API key**:
```bash
# Check if set
echo $GEMINI_API_KEY

# Set if missing
export GEMINI_API_KEY="your-key-here"
```

**Import errors**:
The slide generation script automatically checks and installs dependencies when invoked. If manual intervention is needed:
```bash
# Install required packages manually
pip install google-genai Pillow
```

**Generation failures**:
- Review error message from sub-agent
- Check API quota and rate limits
- Verify prompt isn't too long
- Try simplifying visual requirements
- Retry with adjusted parameters

**Style inconsistency**:
- Ensure reference images are being passed correctly
- Verify style requirements are clear and specific
- Add more explicit style consistency instructions to prompts

## File Organization

All presentation files are saved in a single directory:

```
ppt-output/
└── [presentation-name]/
    ├── requirements.json       # Phase 1 output
    ├── brief-outline.md        # Phase 2 output
    ├── detailed-outline.md     # Phase 3 output
    ├── slide_01.png            # Phase 4 outputs
    ├── slide_02.png
    ├── slide_03.png
    └── ...
```

**User can edit files between phases**:
- After Phase 1: Edit `requirements.json` before proceeding
- After Phase 2: Edit `brief-outline.md` before proceeding
- After Phase 3: Edit `detailed-outline.md` before generation

**To use edited files**: Simply read them from disk before proceeding to next phase.

## Best Practices

### Phase 1-3 (Design - You Execute)
1. **Ask focused questions** - One category at a time, don't overwhelm
2. **Save after each phase** - Write files to disk immediately
3. **Present summaries** - Show user key points, not full JSON/markdown
4. **Iterate quickly** - Direct feedback loop, no agent overhead
5. **Check for edits** - Read files from disk before next phase (user may have edited)

### Phase 4 (Generation - Delegate to Sub-agents)
1. **Generate sequentially** - Always in order (1, 2, 3, ..., N)
2. **Pass reference images** - Each slide uses previous as style reference
3. **Report progress** - Update user after each slide
4. **Handle errors gracefully** - Retry with adjusted parameters if needed
5. **Read from detailed-outline.md** - Use the saved file as source of truth

**Note**: The slide generation script automatically handles dependency checking and installation during execution.

### For Quality Results
1. **Complete requirements** - Incomplete specs lead to poor results
2. **Specific visual descriptions** - Vague outlines produce inconsistent slides
3. **Clear narrative flow** - Each slide should connect to previous/next
4. **Consistent color palette** - Define and maintain throughout
5. **User approval gates** - Don't proceed without confirmation

## Example Session Flow

**User**: "帮我创建一个关于Q4营销成果的PPT"

**You**: "I'll help you create a PPT about Q4 marketing results. Let me gather your requirements."

[You ask questions conversationally]

**You**: "Who is the target audience?"
**User**: "Executive team"
**You**: "What's the main goal?"
**User**: "Show our achievements and justify budget"
**You**: "Preferred visual style?"
**User**: "Professional, data-driven, use company colors"

[Continue interview, then create requirements.json]

**You**: "I've saved the requirements. Here's a summary: [key points]. Does this look correct?"
**User**: "Yes"

**You**: "Great! Now I'll create a brief outline..."

[You create brief-outline.md and present it]

**You**: "I've outlined 12 slides covering achievements, metrics, challenges, and next steps. Should we adjust anything?"
**User**: "Add a slide about team growth"
**You**: "Done. I've updated the outline."

[You update brief-outline.md]

**User**: "Perfect"

**You**: "Now I'll create the detailed specifications..."

[You create detailed-outline.md]

**You**: "I've specified exact content and visuals for each slide. The detailed outline is saved. Please review."
**User**: "Looks good, let's generate"

**You**: "Starting generation..."

[You invoke sub-agent for each slide]

**You**: "✓ Slide 1/12 generated: Q4 Marketing Results"
**You**: "✓ Slide 2/12 generated: Executive Summary"
[...]
**You**: "✓ Slide 12/12 generated: Q1 Priorities"

**You**: "Done! All files are in ./ppt-output/q4-marketing-results/"

## Limitations and Considerations

1. **Image-based output**: Slides are generated as images (.png), not editable .pptx files
2. **Style consistency**: While reference images help, some variation may occur across slides
3. **Text rendering**: Complex text layouts may not always render perfectly
4. **Generation time**: Each slide takes 10-30 seconds, so larger presentations require patience
5. **API costs**: Each slide generation consumes API quota
6. **Iteration limits**: Extensive regeneration increases costs

## Tips for Success

**For better requirements gathering**:
- Ask specific questions about audience and purpose
- Clarify presentation style early
- Get examples of preferred visual styles if possible

**For better outlines**:
- Ensure logical flow and clear transitions
- Balance content across slides (avoid overcrowding)
- Include specific data and messages, not vague descriptions

**For better slide generation**:
- Be very specific about visual requirements
- Describe colors, composition, and mood clearly
- Use concrete examples in prompts
- Reference successful previous slides

**For visual consistency**:
- Establish strong style in Slide 1
- Always pass reference images for subsequent slides
- Use consistent color and typography descriptions
- Describe recurring design elements clearly

## Troubleshooting

**Slides look inconsistent**:
- Check that reference images are being passed
- Add more explicit style consistency instructions
- Describe the visual style more specifically in detailed outline

**Content doesn't match specs**:
- Make prompts more specific and detailed
- Break complex slides into simpler components
- Review and adjust visual requirements

**Generation fails repeatedly**:
- Check API key and quota
- Simplify visual requirements
- Reduce prompt complexity
- Check for rate limiting

**User unhappy with results**:
- Gather more specific feedback
- Iterate on the detailed outline
- Regenerate problematic slides with adjusted specs
- Consider adjusting overall style requirements

## Summary

**Your responsibilities by phase**:

**Phases 1-3 (You execute)**:
1. Interview user conversationally
2. Create requirements.json, brief-outline.md, detailed-outline.md
3. Save files after each phase
4. Get user approval before proceeding
5. Check for user edits before next phase

**Phase 4 (Delegate to sub-agent)**:
1. Read detailed-outline.md from disk
2. Invoke sub-agent for each slide sequentially
3. Pass reference images for consistency
4. Report progress to user
5. Handle errors and retry if needed

**Remember**: Phases 1-3 are interactive design work you do directly. Phase 4 is bulk generation you delegate to sub-agents.
