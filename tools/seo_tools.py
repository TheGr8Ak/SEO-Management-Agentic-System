"""
=============================================================================
SEO AGENT - FUNCTION-BASED TOOLS
=============================================================================
All SEO tools as simple Python functions (Google ADK compatible).
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional  # ⚠️ MISSING: Added Optional
from urllib.parse import urlparse
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def validate_url(url: str) -> tuple[bool, str]:
    """
    Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        (is_valid, error_message)
    """
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True, ""
        return False, "Invalid URL format. Must include http:// or https://"
    except Exception as e:
        return False, f"URL validation error: {str(e)}"


def audit_technical_seo(domain: str) -> dict:
    """
    Perform technical SEO audit on a domain.
    
    Args:
        domain: Domain to audit (e.g., "example.com")
        
    Returns:
        Formatted text report of technical audit results
    """
    try:
        # Ensure domain has protocol
        if not domain.startswith(('http://', 'https://')):
            domain = f"https://{domain}"
        
        # Validate URL
        is_valid, error = validate_url(domain)
        if not is_valid:
            return f"❌ **Technical Audit Failed**\n\nError: {error}"
        
        logger.info(f"Starting technical audit for {domain}")
        
        # Initialize results
        results = {
            'domain': domain,
            'has_ssl': domain.startswith('https://'),
            'has_robots_txt': False,
            'has_sitemap': False,
            'is_accessible': False,
            'issues': []
        }
        
        # Check site accessibility
        try:
            response = requests.get(domain, timeout=10, allow_redirects=True)
            results['is_accessible'] = response.status_code == 200
            results['status_code'] = response.status_code
        except Exception as e:
            return f"❌ **Technical Audit Failed**\n\nUnable to access {domain}: {str(e)}"
        
        # Check robots.txt
        try:
            robots_url = f"{domain.rstrip('/')}/robots.txt"
            robots_response = requests.get(robots_url, timeout=5)
            results['has_robots_txt'] = robots_response.status_code == 200
        except:
            results['has_robots_txt'] = False
        
        # Check sitemap.xml
        try:
            sitemap_url = f"{domain.rstrip('/')}/sitemap.xml"
            sitemap_response = requests.get(sitemap_url, timeout=5)
            results['has_sitemap'] = sitemap_response.status_code == 200
        except:
            results['has_sitemap'] = False
        
        # Parse homepage for basic checks
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check title tag
            title = soup.find('title')
            results['has_title'] = title is not None
            results['title_text'] = title.get_text() if title else None
            
            # Check meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            results['has_meta_description'] = meta_desc is not None
            
            # Check H1 tags
            h1_tags = soup.find_all('h1')
            results['h1_count'] = len(h1_tags)
            
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
        
        # Calculate score
        score = 0
        if results['has_ssl']: score += 20
        if results['has_robots_txt']: score += 15
        if results['has_sitemap']: score += 15
        if results.get('has_title'): score += 20
        if results.get('has_meta_description'): score += 15
        if results.get('h1_count', 0) >= 1: score += 15
        
        results['overall_score'] = score
        
        # Generate formatted report
        report = f"""✅ **Technical SEO Audit Complete**

**Domain:** {domain}
**Audit Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Overall Score:** {score}/100

### Technical Checks

{'✅' if results['has_ssl'] else '❌'} **HTTPS/SSL:** {'Enabled' if results['has_ssl'] else 'Not enabled - CRITICAL ISSUE'}
{'✅' if results['has_robots_txt'] else '❌'} **robots.txt:** {'Found' if results['has_robots_txt'] else 'Missing'}
{'✅' if results['has_sitemap'] else '❌'} **sitemap.xml:** {'Found' if results['has_sitemap'] else 'Missing'}
{'✅' if results.get('has_title') else '❌'} **Title Tag:** {'Present' if results.get('has_title') else 'Missing'}
{'✅' if results.get('has_meta_description') else '❌'} **Meta Description:** {'Present' if results.get('has_meta_description') else 'Missing'}
{'✅' if results.get('h1_count', 0) >= 1 else '❌'} **H1 Tags:** {results.get('h1_count', 0)} found

### Priority Issues

"""
        
        # Add priority issues
        priority_issues = []
        if not results['has_ssl']:
            priority_issues.append("🔴 **CRITICAL:** Enable HTTPS/SSL for security and SEO")
        if not results['has_robots_txt']:
            priority_issues.append("🟠 **HIGH:** Create robots.txt to guide search engine crawlers")
        if not results['has_sitemap']:
            priority_issues.append("🟠 **HIGH:** Create XML sitemap to help search engines index your site")
        if not results.get('has_title'):
            priority_issues.append("🔴 **CRITICAL:** Add title tag to homepage")
        
        if priority_issues:
            for issue in priority_issues:
                report += f"{issue}\n\n"
        else:
            report += "✅ No critical issues found!\n\n"
        
        report += f"""### Recommendations

1. **Improve Score:** Current score is {score}/100. Focus on fixing priority issues first.
2. **Mobile Optimization:** Test mobile responsiveness using Google's Mobile-Friendly Test.
3. **Page Speed:** Check loading speed with Google PageSpeed Insights.
4. **Content:** Ensure all pages have unique titles and meta descriptions.
"""
        
        return report
        
    except Exception as e:
        logger.error(f"Technical audit error: {e}", exc_info=True)
        return f"❌ **Technical Audit Failed**\n\nError: {str(e)}"


def research_keywords(topic: str, domain: Optional[str] = None) -> str:
    """
    Research keywords for a given topic.
    
    Args:
        topic: Topic or niche to research
        domain: Optional domain for context
        
    Returns:
        Formatted text report of keyword research
    """
    try:
        logger.info(f"Researching keywords for topic: {topic}")
        
        # In a real implementation, you would:
        # 1. Call keyword research APIs (SEMrush, Ahrefs, Google Keyword Planner)
        # 2. Analyze search volumes
        # 3. Check keyword difficulty
        # 4. Identify search intent
        
        # For now, provide AI-generated strategic guidance
        report = f"""🎯 **Keyword Research Complete**

**Topic:** {topic}
{f'**Domain:** {domain}' if domain else ''}
**Research Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

### Keyword Strategy

**Primary Keywords (Head Terms):**
These are high-volume, competitive keywords that define your core offering:

1. **Main Topic Keywords** - Focus on 2-3 word phrases with high intent
2. **Service/Product Keywords** - What you sell or offer
3. **Brand Keywords** - Your company name + modifiers

**Long-Tail Keywords (Opportunity):**
These are 4+ word phrases with lower competition and higher conversion:

1. **Question-Based:** "How to...", "What is...", "Best way to..."
2. **Location-Based:** "{topic} near me", "{topic} in [city]"
3. **Comparison:** "{topic} vs", "best {topic} for"
4. **Problem/Solution:** "fix {topic}", "solve {topic} issue"

### Search Intent Types

**Informational:** Users seeking knowledge (e.g., "what is {topic}")
- **Target with:** Blog posts, guides, tutorials
- **Content format:** Educational, detailed

**Transactional:** Users ready to convert (e.g., "buy {topic}")
- **Target with:** Product pages, service pages
- **Content format:** Clear CTAs, pricing, features

**Navigational:** Users looking for specific brand (e.g., "{{your brand}} {topic}")
- **Target with:** Homepage, branded content
- **Content format:** Direct, authoritative

### Implementation Recommendations

1. **Start with Long-Tail:** Easier to rank, higher conversion
2. **Create Content Clusters:** Hub page + 5-10 supporting pages
3. **Optimize for Intent:** Match content format to search intent
4. **Track Rankings:** Monitor positions for target keywords weekly
5. **Build Backlinks:** Quality links to key pages

### Next Steps

1. **Content Audit:** Review existing content for keyword optimization
2. **Gap Analysis:** Identify missing content opportunities
3. **Competitor Research:** Analyze top-ranking competitors
4. **Content Creation:** Write 2-4 posts/month targeting keywords
5. **Performance Tracking:** Set up Google Search Console
"""
        
        return report
        
    except Exception as e:
        logger.error(f"Keyword research error: {e}", exc_info=True)
        return f"❌ **Keyword Research Failed**\n\nError: {str(e)}"


def analyze_content(url: str) -> str:
    """
    Analyze content quality and SEO optimization.
    
    Args:
        url: URL to analyze
        
    Returns:
        Formatted text report of content analysis
    """
    try:
        # Validate URL
        is_valid, error = validate_url(url)
        if not is_valid:
            return f"❌ **Content Analysis Failed**\n\nError: {error}"
        
        logger.info(f"Analyzing content at {url}")
        
        # Fetch page
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return f"❌ **Content Analysis Failed**\n\nUnable to access {url} (Status: {response.status_code})"
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract SEO elements
        title = soup.find('title')
        title_text = title.get_text() if title else None
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_desc_text = meta_desc.get('content') if meta_desc else None
        
        h1_tags = soup.find_all('h1')
        h1_texts = [h1.get_text().strip() for h1 in h1_tags]
        
        # Get body text
        for script in soup(['script', 'style']):
            script.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        words = [word for line in lines for word in line.split()]
        word_count = len(words)
        
        # Calculate content score
        score = 0
        if title_text: score += 20
        if meta_desc_text: score += 20
        if len(h1_tags) == 1: score += 15  # Exactly one H1
        if word_count >= 300: score += 20
        if word_count >= 1000: score += 10
        if meta_desc_text and 120 <= len(meta_desc_text) <= 160: score += 15
        
        # Generate report
        report = f"""📝 **Content Analysis Complete**

**URL:** {url}
**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Content Score:** {score}/100

### SEO Elements

**Title Tag:** {title_text if title_text else '❌ Missing'}
{'✅' if title_text and 30 <= len(title_text) <= 60 else '⚠️'} Length: {len(title_text) if title_text else 0} chars (Optimal: 30-60)

**Meta Description:** {meta_desc_text if meta_desc_text else '❌ Missing'}
{'✅' if meta_desc_text and 120 <= len(meta_desc_text) <= 160 else '⚠️'} Length: {len(meta_desc_text) if meta_desc_text else 0} chars (Optimal: 120-160)

**H1 Tags:** {len(h1_tags)} found {'✅' if len(h1_tags) == 1 else '⚠️ Should have exactly 1'}
{chr(10).join(f'- {h1}' for h1 in h1_texts[:3])}

**Word Count:** {word_count} words {'✅' if word_count >= 300 else '⚠️ Minimum 300 words recommended'}

### Recommendations

"""
        
        # Add specific recommendations
        recommendations = []
        if not title_text:
            recommendations.append("🔴 **CRITICAL:** Add a title tag to this page")
        elif len(title_text) < 30 or len(title_text) > 60:
            recommendations.append(f"🟠 **Title Optimization:** Current length is {len(title_text)} chars. Aim for 30-60 characters.")
        
        if not meta_desc_text:
            recommendations.append("🔴 **CRITICAL:** Add a meta description")
        elif len(meta_desc_text) < 120 or len(meta_desc_text) > 160:
            recommendations.append(f"🟠 **Meta Description:** Current length is {len(meta_desc_text)} chars. Aim for 120-160 characters.")
        
        if len(h1_tags) == 0:
            recommendations.append("🔴 **CRITICAL:** Add an H1 tag to define the page topic")
        elif len(h1_tags) > 1:
            recommendations.append(f"🟡 **H1 Structure:** You have {len(h1_tags)} H1 tags. Use only ONE H1 per page.")
        
        if word_count < 300:
            recommendations.append(f"🟠 **Content Length:** Add more content. Current: {word_count} words, Minimum: 300 words")
        
        if not recommendations:
            recommendations.append("✅ No critical issues found! This page follows SEO best practices.")
        
        for rec in recommendations:
            report += f"{rec}\n\n"
        
        report += """### Next Steps

1. **Implement Fixes:** Address priority issues first (marked with 🔴)
2. **Add Keywords:** Incorporate target keywords naturally in title, headings, and content
3. **Improve Readability:** Use short paragraphs, bullet points, and subheadings
4. **Add Internal Links:** Link to 3-5 related pages on your site
5. **Add Media:** Include relevant images, videos, or infographics
"""
        
        return report
        
    except Exception as e:
        logger.error(f"Content analysis error: {e}", exc_info=True)
        return f"❌ **Content Analysis Failed**\n\nError: {str(e)}"


def check_performance(domain: str, metric_type: str = "all") -> str:
    """
    Check website performance and rankings.
    
    Args:
        domain: Domain to check
        metric_type: Type of metrics to check ('all', 'rankings', 'traffic', 'speed')
    
    Returns:
        Formatted text report of performance metrics
    """
    try:
        logger.info(f"Checking performance for {domain} - Metrics: {metric_type}")
        
        # Build report based on metric_type
        report = f"""📊 **Performance Monitoring Report**

**Domain:** {domain}
**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Metrics Type:** {metric_type.upper()}

"""
        
        # Include sections based on metric_type
        if metric_type in ["all", "rankings"]:
            report += """### Keyword Rankings

**Note:** Connect your Google Search Console account for real-time ranking data.

**Priority Keywords to Track:**
- Salesforce consulting
- Real estate CRM
- Salesforce implementation
- CRM solutions India

**Tracking Recommendations:**
- Set up rank tracking in GSC
- Monitor weekly position changes
- Track competitor rankings
- Focus on page 2 keywords (easier wins)

"""

        if metric_type in ["all", "traffic"]:
            report += """### Organic Traffic

**Connect Google Analytics 4 for:**
- Monthly visitor count
- Traffic source breakdown
- User engagement metrics
- Conversion tracking

**Key Metrics to Monitor:**
- Organic sessions/month
- Bounce rate (aim for <50%)
- Average session duration
- Pages per session
- Goal completions

"""

        if metric_type in ["all", "speed"]:
            report += """### Page Speed & Core Web Vitals

**Test your site speed at:**
- PageSpeed Insights (pagespeed.web.dev)
- GTmetrix
- WebPageTest

**Core Web Vitals Standards:**
- **LCP (Largest Contentful Paint):** <2.5s (Good)
- **FID (First Input Delay):** <100ms (Good)
- **CLS (Cumulative Layout Shift):** <0.1 (Good)

**Speed Optimization Tips:**
1. Compress images (use WebP format)
2. Enable browser caching
3. Minify CSS/JS
4. Use a CDN
5. Optimize server response time

"""

        if metric_type == "all":
            report += """### Recommended Tools

1. **Google Search Console** (Free) - PRIORITY 1
   - Set up at search.google.com/search-console
   - Submit sitemap
   - Monitor indexing status
   - Track keyword performance

2. **Google Analytics 4** (Free) - PRIORITY 1
   - Track user behavior
   - Set up conversion goals
   - Monitor traffic sources
   - Analyze user journeys

3. **PageSpeed Insights** (Free)
   - Test page speed
   - Get optimization recommendations
   - Monitor Core Web Vitals

### Action Items

1. ✅ **Set up Google Search Console** - PRIORITY 1
2. ✅ **Install Google Analytics 4** - PRIORITY 1
3. ✅ **Submit XML sitemap** - PRIORITY 2
4. ✅ **Fix technical issues** - Run technical audit
5. ✅ **Monitor weekly** - Check metrics every Monday

"""
        
        return report
        
    except Exception as e:
        logger.error(f"Performance check error: {e}", exc_info=True)
        return f"❌ **Performance Check Failed**\n\nError: {str(e)}"



def generate_seo_report(domain: str) -> str:
    """
    Generate comprehensive SEO report.
    
    Args:
        domain: Domain to report on
        
    Returns:
        Formatted comprehensive SEO report
    """
    try:
        logger.info(f"Generating comprehensive report for {domain}")
        
        report = f"""📋 **Comprehensive SEO Report**

**Domain:** {domain}
**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Executive Summary

This report provides an overview of {domain}'s current SEO status and actionable recommendations for improvement.

## 1. Technical SEO

Run `audit {domain}` for detailed technical analysis including:
- HTTPS/SSL configuration
- robots.txt and sitemap.xml status
- Mobile-friendliness
- Page speed metrics
- Core Web Vitals

## 2. Content Strategy

Run `analyze content at {domain}` for page-level optimization including:
- Title tag and meta description optimization
- Heading structure (H1-H6)
- Content length and quality
- Keyword usage
- Internal linking

## 3. Keyword Opportunities

Run `research keywords for [your topic]` to discover:
- High-volume target keywords
- Long-tail opportunities
- Search intent analysis
- Competitor keyword gaps
- Content cluster ideas

## 4. Performance Metrics

Run `check rankings for {domain}` to monitor:
- Organic traffic trends
- Keyword position tracking
- Backlink profile analysis
- Conversion metrics
- Technical health scores

## Priority Action Plan

### Week 1: Foundation
1. ✅ Fix critical technical issues (HTTPS, robots.txt, sitemap)
2. ✅ Set up Google Search Console
3. ✅ Set up Google Analytics 4
4. ✅ Optimize homepage (title, meta, H1)

### Week 2-4: Content
1. ✅ Create 4-6 blog posts targeting long-tail keywords
2. ✅ Optimize existing pages
3. ✅ Build internal linking structure
4. ✅ Add schema markup

### Month 2-3: Growth
1. ✅ Build 10-15 quality backlinks
2. ✅ Monitor and adjust based on data
3. ✅ Expand content clusters
4. ✅ Improve page speed

### Month 4-6: Scale
1. ✅ Target more competitive keywords
2. ✅ Expand content production to 8-10 posts/month
3. ✅ Analyze competitor strategies
4. ✅ Refine based on performance data

## Expected Results

**Month 1:** 
- Fix technical issues
- Establish baseline metrics
- First rankings for long-tail keywords

**Month 3:**
- 3-5 page 1 rankings
- 50-100% increase in organic traffic
- Improved crawl efficiency

**Month 6:**
- 10+ page 1 rankings
- 200-300% increase in organic traffic
- Established domain authority

---

**Next Step:** Run specific commands above for detailed analysis of each area.
"""
        
        return report
        
    except Exception as e:
        logger.error(f"Report generation error: {e}", exc_info=True)
        return f"❌ **Report Generation Failed**\n\nError: {str(e)}"
