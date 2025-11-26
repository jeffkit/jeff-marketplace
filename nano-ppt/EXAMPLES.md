# Nano-PPT Usage Examples

This document provides example use cases and expected workflows for the nano-ppt plugin.

## Example 1: Marketing Results Presentation

### User Request
```
User: 帮我创建一个关于Q4营销成果的PPT,要展示给管理层看
```

### Phase 1: Requirements Gathering

**Agent Questions**:
```
1. What are the key Q4 marketing results you want to highlight?
   - User: 我们增长了32%，超过了目标

2. How many slides do you need?
   - User: 大概10-12张吧

3. What style would work best for executives?
   - User: 要专业的商务风格，数据驱动

4. Any specific color scheme?
   - User: 用我们的品牌色，橙色和粉色
```

**Output Requirements JSON**:
```json
{
  "presentation_overview": {
    "topic": "Q4 Marketing Results",
    "target_audience": "Executive Leadership Team",
    "key_message": "Q4 exceeded targets with 32% growth",
    "total_slides": 12
  },
  "content_requirements": {
    "main_sections": [
      "Executive Summary",
      "Key Metrics",
      "Digital Performance",
      "Brand Growth",
      "Challenges",
      "Q1 Priorities"
    ],
    "specific_requirements": "Include specific numbers and ROI data",
    "data_examples": "32% growth, conversion rates, brand awareness metrics"
  },
  "style_requirements": {
    "presentation_style": "Professional corporate",
    "visual_style": "Modern data-driven",
    "color_scheme": "Orange and pink brand colors",
    "tone": "Confident and professional",
    "image_style": "Clean infographics and data visualizations"
  },
  "structural_requirements": {
    "narrative_flow": "Results → Evidence → Implications",
    "transition_style": "Sequential and cumulative",
    "aspect_ratio": "16:9",
    "text_density": "Moderate - key points with supporting data"
  }
}
```

### Phase 2: Brief Outline

**Sample Slides**:
```markdown
### Slide 1: Title & Key Highlights
**Main Idea**: Q4 Marketing Results overview with headline numbers
**Transition**: Opening slide, sets positive tone

### Slide 2: Executive Summary
**Main Idea**: Three key wins - Digital success, Brand growth, Acquisition efficiency
**Transition**: Provides roadmap for subsequent deep-dives

### Slide 3: Q4 Goals vs. Results
**Main Idea**: Visual comparison showing exceeded KPIs
**Transition**: Validates success, sets up explanation
```

### Phase 3: Detailed Outline

**Sample Detailed Slide Spec**:
```markdown
## Slide 3: Q4 Goals vs. Results

### Content Specifications
**Slide Title**: "Q4 Goals vs. Results"
**Main Message**: We exceeded all major KPIs

**Text Content**:
Left side (Goals):
- Digital Growth: 25%
- Brand Awareness: +15pt
- New Customers: 5,000
- Revenue: $1.8M

Right side (Results):
- Digital Growth: 32% ✓
- Brand Awareness: +23pt ✓
- New Customers: 6,200 ✓
- Revenue: $2.4M ✓

### Visual Specifications
**Layout Type**: Split comparison layout

**Image Requirements**:
- **Subject**: Side-by-side comparison with green checkmarks
- **Style**: Clean infographic with bold numbers
- **Composition**: Symmetrical split with clear hierarchy
- **Colors**: Green for exceeded goals, orange/pink accents
- **Elements**: Upward arrows, positive indicators

**Typography**: Large bold numbers, smaller labels, green checkmarks
```

### Phase 4: Slide Generation

**Generated Files**:
```
./ppt-output/q4-marketing-results/
├── slide_01.png  # Title & Key Highlights
├── slide_02.png  # Executive Summary
├── slide_03.png  # Q4 Goals vs. Results
├── slide_04.png  # Digital Campaign Performance
├── slide_05.png  # Brand Awareness Growth
├── slide_06.png  # Customer Acquisition Metrics
├── slide_07.png  # Revenue Breakdown
├── slide_08.png  # Channel Performance
├── slide_09.png  # Market Share Analysis
├── slide_10.png  # Challenges & Learnings
├── slide_11.png  # ROI Summary
└── slide_12.png  # Q1 Priorities
```

---

## Example 2: Product Launch Presentation

### User Request
```
User: I need to create a slide deck for our new product launch next week
```

### Phase 1: Requirements Gathering

**Agent Questions**:
```
1. What product are you launching?
   - User: A new AI-powered analytics dashboard

2. Who's the audience?
   - User: Potential customers and press

3. How many slides?
   - User: Around 15 slides

4. What style?
   - User: Modern, innovative, tech-forward

5. Key message?
   - User: This dashboard makes data analysis 10x faster
```

**Output Requirements**:
```json
{
  "presentation_overview": {
    "topic": "AI-Powered Analytics Dashboard Launch",
    "target_audience": "Potential customers and press",
    "key_message": "10x faster data analysis with AI",
    "total_slides": 15
  },
  "style_requirements": {
    "presentation_style": "Product showcase",
    "visual_style": "Modern tech-forward",
    "color_scheme": "Blue and purple tech gradients",
    "tone": "Innovative and exciting",
    "image_style": "Product screenshots and futuristic tech imagery"
  }
}
```

### Brief Outline Structure

```markdown
1. Title slide
2. Problem statement
3. Market opportunity
4. Solution overview
5-8. Key features (4 slides)
9-10. Use cases
11. Pricing
12. Demo preview
13. Customer testimonials
14. Competitive advantage
15. Call to action
```

---

## Example 3: Educational Presentation

### User Request
```
User: Create a presentation teaching basic Python programming to beginners
```

### Requirements Summary

```json
{
  "presentation_overview": {
    "topic": "Python Programming Basics",
    "target_audience": "Complete beginners",
    "key_message": "Python is easy to learn and powerful",
    "total_slides": 20
  },
  "style_requirements": {
    "presentation_style": "Educational",
    "visual_style": "Friendly and approachable",
    "color_scheme": "Python blue and yellow",
    "tone": "Encouraging and supportive",
    "image_style": "Diagrams, code examples, friendly illustrations"
  },
  "structural_requirements": {
    "narrative_flow": "Progressive learning - simple to complex",
    "transition_style": "Each slide builds on previous concepts"
  }
}
```

### Slide Examples

```
1. What is Python?
2. Why Learn Python?
3. Setting Up Python
4. Your First Program: Hello World
5. Variables Explained
6. Data Types: Numbers
7. Data Types: Strings
8. Data Types: Lists
9. Conditional Statements: If/Else
10. Loops: For Loops
...
```

---

## Example 4: Startup Pitch Deck

### User Request
```
User: I need a pitch deck for investors - we're a fintech startup
```

### Requirements Summary

```json
{
  "presentation_overview": {
    "topic": "Fintech Startup Investment Pitch",
    "target_audience": "Venture capital investors",
    "key_message": "Disrupting payments with blockchain technology",
    "total_slides": 10
  },
  "style_requirements": {
    "presentation_style": "Investment pitch",
    "visual_style": "Professional but bold",
    "color_scheme": "Dark background with gold/green accents",
    "tone": "Confident and compelling",
    "image_style": "Charts, market data, product mockups"
  }
}
```

### Standard Pitch Deck Structure

```markdown
1. Company vision
2. Problem
3. Solution
4. Market opportunity
5. Business model
6. Traction & metrics
7. Competition
8. Team
9. Financials & ask
10. Thank you & contact
```

---

## Tips for Different Use Cases

### Corporate/Business Presentations
- Use professional color schemes
- Include lots of data and charts
- Formal language and tone
- Clean, minimalist designs

### Product Launches
- Highlight product visuals prominently
- Use dynamic, energetic imagery
- Focus on benefits, not just features
- Include customer success stories

### Educational Content
- Progressive complexity
- Clear, simple visuals
- Lots of examples and diagrams
- Friendly, approachable tone

### Investor Pitches
- Tell a compelling story
- Back claims with data
- Professional but memorable design
- Clear ask and next steps

### Conference Talks
- Large, readable text
- Minimal text per slide
- High-quality images
- Strong visual hierarchy

---

## Common Customizations

### Aspect Ratio Changes

Default is 16:9, but specify others:
```
User: Make it 4:3 for the old projector in our conference room
```

### Style Adjustments

```
User: Can we make it more colorful and fun?
User: Let's use a darker background theme
User: I prefer minimalist design with lots of white space
```

### Content Iterations

```
User: Add a slide about our company history before the results
User: Remove the challenges slide, executives don't want to see that
User: Can we split slide 5 into two slides? It's too dense
```

---

## Script Usage Examples

### Direct Script Usage (for testing)

**Generate a single slide**:
```bash
python3 skills/nano-ppt/scripts/slide_generator.py \
  "Create a professional title slide for 'Q4 Marketing Results' presentation. Bold title text, company logo space, clean modern design with orange and pink gradient background." \
  ./test-output/slide_01.png \
  --aspect-ratio 16:9
```

**Generate with reference image**:
```bash
python3 skills/nano-ppt/scripts/slide_generator.py \
  "Create a data visualization slide showing Q4 goals vs results with green checkmarks." \
  ./test-output/slide_02.png \
  --aspect-ratio 16:9 \
  --reference-image ./test-output/slide_01.png
```

**Generate with context JSON**:
```bash
python3 skills/nano-ppt/scripts/slide_generator.py \
  "Executive summary slide with three key wins" \
  ./test-output/slide_03.png \
  --aspect-ratio 16:9 \
  --reference-image ./test-output/slide_02.png \
  --context '{"ppt_overview": "Q4 Marketing Results", "slide_title": "Executive Summary", "style_requirements": "Professional corporate with orange/pink branding"}'
```

---

## Expected Timelines

- **Requirements gathering**: 2-5 minutes (depends on user responsiveness)
- **Brief outline creation**: 30-60 seconds
- **Detailed outline creation**: 1-2 minutes
- **Slide generation**:
  - Per slide: 10-30 seconds
  - 10 slides: ~3-5 minutes
  - 20 slides: ~6-10 minutes

Total time for typical 12-slide presentation: **10-15 minutes**
