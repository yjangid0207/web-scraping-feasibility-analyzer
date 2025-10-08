# Web Scraping Feasibility Analyzer

A comprehensive tool for analyzing the feasibility of web scraping projects. This analyzer evaluates websites for scraping compatibility, anti-bot measures, technical challenges, and provides detailed reports with actionable recommendations.

## Features

- **Comprehensive Website Analysis**: Evaluates robots.txt, rate limiting, anti-bot detection systems
- **Technical Assessment**: Analyzes JavaScript rendering requirements, authentication needs, and data extraction complexity
- **Multi-format Reports**: Generates analysis reports in Markdown, HTML, PDF, and DOCX formats
- **Executive Summaries**: Provides concise summaries for stakeholders
- **Site Mapping**: Creates detailed sitemaps for target websites
- **Playwright Integration**: Uses Playwright MCP for browser automation and dynamic content analysis
- **Flexible Output**: Supports multiple output formats for different use cases

## Project Structure

```
web-scraping-feasibility-analyzer/
├── analysis-report/          # Generated analysis reports
├── .playwright-mcp/         # Playwright MCP configuration
├── shared_docx_converter.py  # Markdown to DOCX conversion utility
└── README.md                # This file
```

## Playwright MCP Integration

This tool integrates with Playwright MCP (Model Context Protocol) for advanced browser automation and dynamic content analysis:

- **Browser Automation**: Automated testing of JavaScript-heavy websites
- **Dynamic Content Analysis**: Evaluates content that requires browser rendering
- **Anti-bot Detection**: Tests various protection mechanisms in real browser environments
- **Performance Monitoring**: Measures page load times and resource usage
- **Screenshot Capture**: Visual documentation of website behavior

## Installation

### Prerequisites

```bash
# Python 3.7+ required
python --version

# Install required dependencies
pip install python-docx pypandoc

# Install Playwright for browser automation
pip install playwright
playwright install
```

### Playwright MCP Setup

To enable advanced browser automation features with Claude Code, install the Playwright MCP integration:

```bash
# Add Playwright MCP to Claude Code
claude mcp add playwright npx @playwright/mcp@latest
```

This integration provides enhanced capabilities for:
- Real-time browser automation during analysis
- Dynamic content testing and evaluation
- Anti-bot detection mechanism testing
- Live website interaction and data extraction validation

### Dependencies

- **python-docx**: For native DOCX conversion (recommended)
- **pypandoc**: Fallback DOCX conversion method
- **playwright**: Browser automation for dynamic content analysis
- **playwright-mcp**: Model Context Protocol integration for Playwright

## Usage

### Converting Markdown Reports to DOCX

```bash
# Convert a single markdown file
python shared_docx_converter.py report.md

# Convert with custom output directory
python shared_docx_converter.py report.md /path/to/output/

# Convert all markdown files in a directory
python shared_docx_converter.py --dir analysis-report/
```

### Browser Automation Analysis

The tool uses Playwright MCP for comprehensive website analysis:

- **Dynamic Testing**: Automated browser testing of target websites
- **JavaScript Evaluation**: Analysis of client-side rendering requirements
- **Protection Testing**: Detection of anti-bot and security measures
- **Performance Metrics**: Page load times and resource utilization

## Report Contents

Each analysis includes:

- ✅ **Feasibility Score**: Overall scraping difficulty rating
- 🛡️ **Security Assessment**: Anti-bot and protection mechanisms
- ⚡ **Performance Analysis**: Rate limiting and request handling
- 🔧 **Technical Requirements**: Tools and approaches needed
- 📋 **Risk Assessment**: Legal and technical risks
- 💡 **Recommendations**: Best practices and implementation strategies

## Features of the DOCX Converter

- **Native Python Implementation**: Uses python-docx for optimal formatting
- **Fallback Support**: Pypandoc as backup conversion method
- **Markdown Parsing**: Supports headers, lists, bold text, tables
- **Batch Processing**: Convert multiple files at once
- **Error Handling**: Graceful failure with detailed error messages

## Contributing

This is a defensive security tool designed for legitimate web scraping feasibility analysis. Contributions should focus on:

- Improving analysis accuracy
- Testing with proxies 
- Enhancing security assessments
- Documentation improvements

