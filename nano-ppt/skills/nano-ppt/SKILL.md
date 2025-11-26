---
name: nano-ppt
description: AI-powered PPT presentation creation using Google's Gemini image generation (nano-banana). Use this skill when users want to create PowerPoint presentations, slides, or visual presentations. Triggers include requests like "创建PPT", "制作演示文稿", "帮我做个presentation", "make a slide deck", or any request to create presentation slides. The skill orchestrates the entire workflow from requirements gathering through slide generation.
---

# Nano-PPT: AI-Powered Presentation Creator

This skill creates professional PPT presentations using Google's Gemini image generation model (gemini-2.5-flash-image, also known as "nano-banana"). It orchestrates the complete workflow from understanding user requirements to generating individual slides as images.

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

**Phase 1: Requirements Gathering** → **Phase 2: Brief Outline** → **Phase 3: Detailed Outline** → **Phase 4: Slide Generation**

Each phase uses specialized sub-agents and requires user approval before proceeding to the next phase.

## Your Role as Orchestrator

You are the **project manager**, not the executor. Your responsibilities:

1. **Delegate work** to sub-agents via the Task tool
2. **Review outputs** critically - don't blindly accept sub-agent results
3. **Manage user interactions** - gather approvals, handle feedback
4. **Make continuation decisions** - determine when to proceed to next phase
5. **Ensure quality** - verify outputs meet requirements at each stage
6. **Handle errors** - troubleshoot issues and retry if needed

**CRITICAL**: Do NOT execute the work yourself. Always use sub-agents for each phase.

## Detailed Workflow

### Phase 1: Requirements Gathering

**Objective**: Understand what presentation the user wants to create.

**Process**:
1. Invoke the `nanoppt-requirements` sub-agent
2. The agent will conduct a conversational interview with the user
3. Agent returns a structured JSON requirements document
4. You review and confirm the requirements with the user

**Sub-agent invocation**:
```
Use Task tool with:
- subagent_type: "general-purpose"
- prompt: Read and follow the instructions in agents/nanoppt-requirements.md to gather presentation requirements from the user. Return a complete JSON requirements document.
```

**Expected output**: JSON document with presentation overview, content requirements, style requirements, and structural requirements.

**Quality check**:
- All required fields populated?
- Requirements clear and specific?
- User confirmed requirements are correct?

**Proceed to Phase 2 only after** user confirms requirements are complete and accurate.

### Phase 2: Brief Outline Creation

**Objective**: Create a high-level outline showing slide titles, main ideas, and transitions.

**Process**:
1. Invoke the `nanoppt-brief-outline` sub-agent with the requirements
2. Agent creates brief outline with slide structure and narrative flow
3. You present the outline to the user for feedback
4. Iterate based on user feedback until approved

**Sub-agent invocation**:
```
Use Task tool with:
- subagent_type: "general-purpose"
- prompt: Read and follow the instructions in agents/nanoppt-brief-outline.md. Create a brief outline based on these requirements: [paste requirements JSON]. Return the brief outline in markdown format.
```

**Expected output**: Markdown outline with:
- Presentation overview and narrative style
- Each slide's title, main idea, and transition relationship
- Narrative flow summary

**Quality check**:
- Logical flow and structure?
- Appropriate number of slides?
- Clear transitions between slides?
- Matches user's requirements?

**User feedback loop**:
- Ask: "Does this structure and flow make sense?"
- Ask: "Should any slides be added, removed, or reordered?"
- Iterate until user approves

**Proceed to Phase 3 only after** user approves the brief outline structure.

### Phase 3: Detailed Outline Creation

**Objective**: Expand the brief outline into production-ready specifications with complete content and visual requirements for each slide.

**Process**:
1. Invoke the `nanoppt-detailed-outline` sub-agent with approved brief outline and requirements
2. Agent expands each slide with content specs, visual requirements, layout details
3. You present the detailed outline to the user for final approval
4. Make any adjustments based on feedback

**Sub-agent invocation**:
```
Use Task tool with:
- subagent_type: "general-purpose"
- prompt: Read and follow the instructions in agents/nanoppt-detailed-outline.md. Create a detailed outline based on this approved brief outline: [paste brief outline] and these requirements: [paste requirements]. Return the complete detailed outline in markdown format.
```

**Expected output**: Markdown outline with:
- Complete content specifications for each slide (exact text, data, messages)
- Detailed visual specifications (layout, image requirements, colors, typography)
- Design notes and consistency guidelines
- Production notes (color palette, style consistency strategy)

**Quality check**:
- Every slide fully specified?
- Visual requirements actionable and specific?
- Consistency strategy defined?
- Aligns with approved brief outline?

**User feedback loop**:
- Ask: "Is all content accurate and complete?"
- Ask: "Does the visual direction match your expectations?"
- Make adjustments as needed

**Proceed to Phase 4 only after** user approves the detailed outline.

### Phase 4: Slide Generation

**Objective**: Generate each slide as an image file using Google's Gemini model.

**Setup**:
1. Create output directory: `./ppt-output/[presentation-name]/`
2. Verify `GEMINI_API_KEY` environment variable is set
3. Confirm slide generation script is accessible

**Process**:
For each slide in the detailed outline (sequentially):

1. **Invoke the `nanoppt-slide-generator` sub-agent**:
   ```
   Use Task tool with:
   - subagent_type: "general-purpose"
   - prompt: Read and follow the instructions in agents/nanoppt-slide-generator.md. Generate Slide [N] of [Total].

     Slide specifications: [paste this slide's detailed specs]
     Presentation context: [paste overall theme, style, colors]
     Previous slide: [paste previous slide info and path to image]
     Next slide preview: [paste next slide title/main idea]
     Aspect ratio: [from requirements]
     Output path: ./ppt-output/[presentation-name]/slide_[NN].png

     Generate the slide and report the result.
   ```

2. **Track progress**: Update user after each slide is generated
3. **Handle errors**: If generation fails, review error and retry with adjusted parameters
4. **Sequential generation**: Always generate slides in order (1, 2, 3, ..., N)

**Why sequential generation**:
- Each slide references the previous slide's image for style consistency
- Ensures visual coherence across the presentation
- Maintains narrative flow

**Progress reporting**:
After each slide: "✓ Slide [N]/[Total] generated: [title]"

**Final output**:
- All slide images in `./ppt-output/[presentation-name]/`
- Filenames: `slide_01.png`, `slide_02.png`, ..., `slide_NN.png`
- Consistent aspect ratio and visual style

**Quality check**:
- All slides generated successfully?
- Visual consistency maintained?
- Content matches specifications?

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
```bash
# Install required packages
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

Generated presentations are organized as:

```
ppt-output/
├── [presentation-name]/
│   ├── slide_01.png
│   ├── slide_02.png
│   ├── slide_03.png
│   └── ...
```

Optionally save outlines for reference:
```
ppt-output/
├── [presentation-name]/
│   ├── requirements.json
│   ├── brief-outline.md
│   ├── detailed-outline.md
│   ├── slide_01.png
│   └── ...
```

## Best Practices

### For Orchestration
1. **Always use sub-agents** - Don't try to do the work yourself
2. **Review outputs critically** - Verify sub-agent work before presenting to user
3. **Get user approval** at each phase transition
4. **Handle feedback gracefully** - Iterate until user is satisfied
5. **Track state clearly** - Know which phase you're in and what's been approved

### For Quality Results
1. **Gather complete requirements** - Incomplete requirements lead to poor results
2. **Ensure clear specifications** - Vague outlines produce inconsistent slides
3. **Maintain visual consistency** - Always pass reference images (except Slide 1)
4. **Generate sequentially** - Don't skip around or generate in parallel
5. **Verify before proceeding** - Each phase builds on the previous one

### For User Experience
1. **Communicate progress clearly** - Let user know what's happening
2. **Ask for feedback proactively** - Don't assume approval
3. **Explain the process** - Help user understand the workflow
4. **Show examples** when requirements are unclear
5. **Be patient with iterations** - Quality takes refinement

## Example Session Flow

**User**: "帮我创建一个关于Q4营销成果的PPT"

**You**: "I'll help you create a PPT presentation about Q4 marketing results. Let me start by gathering your requirements."

[Invoke nanoppt-requirements agent]

**Agent**: [Conducts interview, returns requirements JSON]

**You**: "Based on our discussion, here's what I understand: [summarize key requirements]. Is this correct?"

**User**: "Yes, that's right."

**You**: "Great! Now I'll create a brief outline showing the slide structure and flow."

[Invoke nanoppt-brief-outline agent]

**You**: [Present brief outline] "Does this structure and flow make sense? Should we adjust anything?"

**User**: "Can we add a slide about challenges we faced?"

**You**: "Absolutely. Let me update the outline."

[Re-invoke with feedback, get revised outline]

**User**: "Perfect, this looks good."

**You**: "Excellent! Now I'll create the detailed outline with complete content and visual specifications for each slide."

[Invoke nanoppt-detailed-outline agent]

**You**: [Present detailed outline] "Please review the content and visual direction. Is everything accurate?"

**User**: "Yes, let's proceed."

**You**: "Perfect! I'll now generate the slides. This will take a few minutes as I create each slide sequentially to maintain visual consistency."

[Invoke nanoppt-slide-generator for each slide sequentially]

**You**: "✓ Slide 1/12 generated: Title & Key Highlights"
**You**: "✓ Slide 2/12 generated: Executive Summary"
[...]
**You**: "✓ Slide 12/12 generated: Next Quarter Priorities"

**You**: "All done! Your presentation is ready in ./ppt-output/q4-marketing-results/ with 12 slides. Each slide maintains consistent visual style and follows the narrative flow we planned."

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

As the orchestrator, your job is to:
1. **Guide the user** through the 4-phase workflow
2. **Delegate work** to specialized sub-agents
3. **Ensure quality** at each phase transition
4. **Manage iterations** based on user feedback
5. **Deliver** a complete presentation with consistent, professional slides

Remember: You coordinate, review, and decide. Sub-agents execute. Users approve and provide feedback.
