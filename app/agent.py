"""
AI agent analysis module for misinformation detection using Google Gemini.

This module provides the core analysis functionality that processes text content
to determine its credibility and potential for being misinformation using
Google's Gemini AI model.
"""

import asyncio
import logging
import os
from typing import Dict, List, Any, Optional
import json
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
MAX_CLAIMS = int(os.getenv("MAX_CLAIMS_TO_ANALYZE", "5"))
ANALYSIS_TIMEOUT = int(os.getenv("ANALYSIS_TIMEOUT_SECONDS", "30"))

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
else:
    logger.warning("GEMINI_API_KEY not found. Using mock responses for development.")
    model = None


async def run_analysis(content: str) -> Dict[str, Any]:
    """
    Analyze text content for misinformation detection using Google Gemini.
    
    This function implements a structured workflow to analyze content:
    1. Deconstruct main claims from the content using Gemini
    2. Query vector databases for relevant context (simulated)
    3. Synthesize results to determine credibility using Gemini
    
    Args:
        content (str): The text content to analyze
        
    Returns:
        Dict[str, Any]: Analysis results containing verdict, explanation, and sources
        
    Raises:
        ValueError: If content is empty or invalid
        Exception: For other analysis errors
    """
    if not content or not content.strip():
        raise ValueError("Content cannot be empty")
    
    logger.info(f"Starting Gemini analysis for content: {content[:100]}...")
    
    try:
        # Step 1: Deconstruct main claims using Gemini (Requirements 4.1)
        claims = await _deconstruct_claims_with_gemini(content)
        logger.info(f"Gemini deconstructed {len(claims)} claims from content")
        
        # Step 2: Query vector database for context (Requirements 4.2)
        # Note: This is simulated for now, but could be replaced with real vector DB
        context_data = await _query_vector_database(claims)
        logger.info(f"Retrieved context data for {len(context_data)} sources")
        
        # Step 3: Synthesize results using Gemini (Requirements 4.3, 4.4)
        analysis_result = await _synthesize_results_with_gemini(claims, context_data, content)
        logger.info(f"Gemini analysis complete with verdict: {analysis_result['verdict']}")
        
        return analysis_result
        
    except Exception as e:
        logger.error(f"Gemini analysis failed: {str(e)}")
        raise


async def _deconstruct_claims_with_gemini(content: str) -> List[str]:
    """
    Deconstruct the main claims from the provided content using Google Gemini.
    
    Uses Gemini to intelligently identify and extract factual claims
    from the text content for further analysis.
    
    Args:
        content (str): The text content to analyze
        
    Returns:
        List[str]: List of identified claims
    """
    logger.info("Deconstructing claims using Gemini...")
    
    if not model:
        # Fallback to simple extraction if Gemini is not available
        logger.warning("Gemini not available, using fallback claim extraction")
        return await _fallback_claim_extraction(content)
    
    try:
        prompt = f"""
        Analyze the following text and extract the main factual claims that can be fact-checked.
        Focus on specific, verifiable statements rather than opinions or subjective statements.
        
        Text to analyze:
        "{content}"
        
        Please respond with a JSON array containing up to {MAX_CLAIMS} of the most important factual claims.
        Each claim should be a clear, standalone statement.
        
        Example format:
        ["Claim 1", "Claim 2", "Claim 3"]
        
        If no factual claims are found, return an empty array: []
        """
        
        # Generate response with timeout
        response = await asyncio.wait_for(
            asyncio.to_thread(model.generate_content, prompt),
            timeout=ANALYSIS_TIMEOUT
        )
        
        # Parse the response
        response_text = response.text.strip()
        logger.debug(f"Gemini claims response: {response_text}")
        
        # Try to parse JSON response
        try:
            # Clean up the response text (remove markdown formatting if present)
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            claims = json.loads(response_text)
            
            if not isinstance(claims, list):
                logger.warning("Gemini response is not a list, using fallback")
                return await _fallback_claim_extraction(content)
            
            # Filter and validate claims
            valid_claims = []
            for claim in claims:
                if isinstance(claim, str) and len(claim.strip()) > 10:
                    valid_claims.append(claim.strip())
            
            logger.info(f"Gemini identified {len(valid_claims)} valid claims")
            return valid_claims[:MAX_CLAIMS]
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Gemini JSON response: {e}")
            return await _fallback_claim_extraction(content)
        
    except asyncio.TimeoutError:
        logger.warning("Gemini claim extraction timed out, using fallback")
        return await _fallback_claim_extraction(content)
    except Exception as e:
        logger.warning(f"Gemini claim extraction failed: {e}, using fallback")
        return await _fallback_claim_extraction(content)


async def _fallback_claim_extraction(content: str) -> List[str]:
    """
    Fallback claim extraction when Gemini is not available.
    
    Args:
        content (str): The text content to analyze
        
    Returns:
        List[str]: List of identified claims
    """
    logger.info("Using fallback claim extraction...")
    
    # Simple rule-based claim extraction
    sentences = content.split('.')
    claims = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20:  # Filter out very short sentences
            # Look for factual claim indicators
            claim_indicators = ['is', 'are', 'was', 'were', 'will', 'can', 'cannot', 'shows', 'proves', 'causes', 'leads to']
            if any(indicator in sentence.lower() for indicator in claim_indicators):
                claims.append(sentence)
    
    logger.info(f"Fallback extraction identified {len(claims)} potential claims")
    return claims[:MAX_CLAIMS]


async def _query_vector_database(claims: List[str]) -> List[Dict[str, Any]]:
    """
    Query vector database for relevant context about the claims.
    
    This simulates querying a vector database to find relevant
    information and sources related to the identified claims.
    
    Args:
        claims (List[str]): List of claims to search for
        
    Returns:
        List[Dict[str, Any]]: Context data from vector database
    """
    logger.info(f"Querying vector database for {len(claims)} claims...")
    
    # Simulate vector database query latency
    await asyncio.sleep(1.0)
    
    context_data = []
    
    for i, claim in enumerate(claims):
        # Simulate vector database response
        context_entry = {
            "claim": claim,
            "similarity_score": 0.85 - (i * 0.1),  # Decreasing relevance
            "source_title": f"Fact Check Source {i + 1}",
            "source_url": f"https://factcheck.example.com/article-{i + 1}",
            "snippet": f"Relevant information about: {claim[:50]}...",
            "credibility_rating": "high" if i < 2 else "medium"
        }
        context_data.append(context_entry)
        
        # Simulate individual query processing time
        await asyncio.sleep(0.2)
    
    logger.info(f"Retrieved {len(context_data)} context entries from vector database")
    return context_data


async def _synthesize_results_with_gemini(claims: List[str], context_data: List[Dict[str, Any]], 
                                        original_content: str) -> Dict[str, Any]:
    """
    Synthesize analysis results using Google Gemini to determine credibility and generate verdict.
    
    This function uses Gemini to analyze the deconstructed claims and context data
    to generate a comprehensive verdict with explanation and source references.
    
    Args:
        claims (List[str]): Identified claims from the content
        context_data (List[Dict[str, Any]]): Context from vector database
        original_content (str): Original content being analyzed
        
    Returns:
        Dict[str, Any]: Final analysis result with verdict, explanation, and sources
    """
    logger.info("Synthesizing results using Gemini...")
    
    if not model:
        # Fallback to simple analysis if Gemini is not available
        logger.warning("Gemini not available, using fallback analysis")
        return await _fallback_result_synthesis(claims, context_data, original_content)
    
    try:
        # Prepare context information for Gemini
        context_summary = _prepare_context_for_gemini(claims, context_data)
        
        prompt = f"""
        You are an expert fact-checker analyzing content for misinformation. 
        
        Original Content:
        "{original_content}"
        
        Identified Claims:
        {json.dumps(claims, indent=2)}
        
        Available Context:
        {context_summary}
        
        Please analyze this content and provide a comprehensive fact-check assessment.
        
        Respond with a JSON object containing:
        {{
            "verdict": "LIKELY_ACCURATE|MOSTLY_ACCURATE|MIXED_ACCURACY|LIKELY_INACCURATE|HIGHLY_QUESTIONABLE",
            "explanation": "Detailed explanation of your analysis and reasoning",
            "credibility_score": 0.0-1.0,
            "key_findings": ["Finding 1", "Finding 2", "Finding 3"]
        }}
        
        Verdict Guidelines:
        - LIKELY_ACCURATE: Content is well-supported by reliable sources
        - MOSTLY_ACCURATE: Content is generally accurate with minor issues
        - MIXED_ACCURACY: Content contains both accurate and questionable elements
        - LIKELY_INACCURATE: Content contains significant inaccuracies
        - HIGHLY_QUESTIONABLE: Content is highly questionable or misleading
        
        Consider:
        - Source credibility and reliability
        - Evidence quality and consistency
        - Potential bias or misleading framing
        - Scientific consensus where applicable
        - Logical consistency of claims
        """
        
        # Generate response with timeout
        response = await asyncio.wait_for(
            asyncio.to_thread(model.generate_content, prompt),
            timeout=ANALYSIS_TIMEOUT
        )
        
        # Parse the response
        response_text = response.text.strip()
        logger.debug(f"Gemini synthesis response: {response_text}")
        
        # Try to parse JSON response
        try:
            # Clean up the response text
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            gemini_result = json.loads(response_text)
            
            # Validate and extract results
            verdict = gemini_result.get("verdict", "MIXED_ACCURACY")
            explanation = gemini_result.get("explanation", "Analysis completed using AI assessment.")
            credibility_score = float(gemini_result.get("credibility_score", 0.5))
            key_findings = gemini_result.get("key_findings", [])
            
            # Ensure credibility score is in valid range
            credibility_score = max(0.0, min(1.0, credibility_score))
            
            # Extract sources from context data
            sources = _extract_sources(context_data)
            
            # Add key findings to explanation if available
            if key_findings:
                explanation += f" Key findings: {'; '.join(key_findings)}."
            
            result = {
                "verdict": verdict,
                "explanation": explanation,
                "sources": sources,
                "credibility_score": credibility_score,
                "claims_analyzed": len(claims),
                "sources_consulted": len(context_data)
            }
            
            logger.info(f"Gemini synthesis complete: {verdict} (score: {credibility_score:.2f})")
            return result
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.warning(f"Failed to parse Gemini synthesis response: {e}")
            return await _fallback_result_synthesis(claims, context_data, original_content)
        
    except asyncio.TimeoutError:
        logger.warning("Gemini synthesis timed out, using fallback")
        return await _fallback_result_synthesis(claims, context_data, original_content)
    except Exception as e:
        logger.warning(f"Gemini synthesis failed: {e}, using fallback")
        return await _fallback_result_synthesis(claims, context_data, original_content)


def _prepare_context_for_gemini(claims: List[str], context_data: List[Dict[str, Any]]) -> str:
    """
    Prepare context information in a format suitable for Gemini analysis.
    
    Args:
        claims (List[str]): Identified claims
        context_data (List[Dict[str, Any]]): Context from vector database
        
    Returns:
        str: Formatted context summary
    """
    if not context_data:
        return "No additional context sources available."
    
    context_lines = []
    for i, context in enumerate(context_data, 1):
        source_title = context.get("source_title", f"Source {i}")
        credibility = context.get("credibility_rating", "unknown")
        similarity = context.get("similarity_score", 0.0)
        snippet = context.get("snippet", "No snippet available")
        
        context_lines.append(f"Source {i}: {source_title} (Credibility: {credibility}, Relevance: {similarity:.2f})")
        context_lines.append(f"  Content: {snippet}")
    
    return "\n".join(context_lines)


async def _fallback_result_synthesis(claims: List[str], context_data: List[Dict[str, Any]], 
                                   original_content: str) -> Dict[str, Any]:
    """
    Fallback result synthesis when Gemini is not available.
    
    Args:
        claims (List[str]): Identified claims
        context_data (List[Dict[str, Any]]): Context from vector database
        original_content (str): Original content being analyzed
        
    Returns:
        Dict[str, Any]: Analysis result
    """
    logger.info("Using fallback result synthesis...")
    
    try:
        # Calculate credibility score based on context data
        credibility_score = await _calculate_credibility_score(claims, context_data)
        
        # Generate verdict based on credibility score
        verdict = _generate_verdict(credibility_score)
        
        # Generate explanation
        explanation = _generate_explanation(claims, context_data, credibility_score, verdict)
        
        # Extract sources from context data
        sources = _extract_sources(context_data)
        
        result = {
            "verdict": verdict,
            "explanation": explanation,
            "sources": sources,
            "credibility_score": credibility_score,
            "claims_analyzed": len(claims),
            "sources_consulted": len(context_data)
        }
        
        logger.info(f"Fallback synthesis complete: {verdict} (score: {credibility_score:.2f})")
        return result
        
    except Exception as e:
        logger.error(f"Fallback synthesis failed: {str(e)}")
        return {
            "verdict": "ERROR",
            "explanation": f"Analysis failed due to processing error: {str(e)}",
            "sources": [],
            "credibility_score": 0.0,
            "claims_analyzed": len(claims) if claims is not None else 0,
            "sources_consulted": len(context_data) if context_data is not None else 0
        }


async def _calculate_credibility_score(claims: List[str], 
                                     context_data: List[Dict[str, Any]]) -> float:
    """
    Calculate credibility score based on claims and context data.
    
    Args:
        claims (List[str]): Identified claims
        context_data (List[Dict[str, Any]]): Context from vector database
        
    Returns:
        float: Credibility score between 0.0 and 1.0
    """
    if not context_data:
        return 0.5  # Neutral score if no context available
    
    # Simulate AI processing
    await asyncio.sleep(0.3)
    
    # Calculate weighted score based on source credibility and similarity
    total_weight = 0.0
    weighted_score = 0.0
    
    for context in context_data:
        similarity = context.get("similarity_score", 0.5)
        credibility_rating = context.get("credibility_rating", "medium")
        
        # Convert credibility rating to numeric score
        credibility_multiplier = {
            "high": 1.0,
            "medium": 0.7,
            "low": 0.3
        }.get(credibility_rating, 0.5)
        
        weight = similarity * credibility_multiplier
        total_weight += weight
        weighted_score += weight * similarity
    
    if total_weight == 0:
        return 0.5
    
    final_score = weighted_score / total_weight
    
    # Add some randomness to simulate AI uncertainty
    import random
    noise = random.uniform(-0.1, 0.1)
    final_score = max(0.0, min(1.0, final_score + noise))
    
    return final_score


def _generate_verdict(credibility_score: float) -> str:
    """
    Generate verdict based on credibility score.
    
    Args:
        credibility_score (float): Calculated credibility score
        
    Returns:
        str: Verdict classification
    """
    if credibility_score >= 0.8:
        return "LIKELY_ACCURATE"
    elif credibility_score >= 0.6:
        return "MOSTLY_ACCURATE"
    elif credibility_score >= 0.4:
        return "MIXED_ACCURACY"
    elif credibility_score >= 0.2:
        return "LIKELY_INACCURATE"
    else:
        return "HIGHLY_QUESTIONABLE"


def _generate_explanation(claims: List[str], context_data: List[Dict[str, Any]], 
                         credibility_score: float, verdict: str) -> str:
    """
    Generate human-readable explanation for the analysis result.
    
    Args:
        claims (List[str]): Analyzed claims
        context_data (List[Dict[str, Any]]): Context data
        credibility_score (float): Calculated score
        verdict (str): Generated verdict
        
    Returns:
        str: Detailed explanation of the analysis
    """
    explanation_parts = []
    
    # Add verdict explanation
    verdict_explanations = {
        "LIKELY_ACCURATE": "The content appears to be largely accurate based on available sources.",
        "MOSTLY_ACCURATE": "The content is generally accurate with some minor concerns.",
        "MIXED_ACCURACY": "The content contains both accurate and questionable elements.",
        "LIKELY_INACCURATE": "The content appears to contain significant inaccuracies.",
        "HIGHLY_QUESTIONABLE": "The content is highly questionable and likely contains misinformation."
    }
    
    explanation_parts.append(verdict_explanations.get(verdict, "Unable to determine accuracy."))
    
    # Add claims analysis
    if claims:
        explanation_parts.append(f"Analysis examined {len(claims)} key claims from the content.")
    
    # Add source information
    if context_data:
        high_credibility_sources = sum(1 for ctx in context_data 
                                     if ctx.get("credibility_rating") == "high")
        explanation_parts.append(f"Consulted {len(context_data)} sources, "
                               f"{high_credibility_sources} of which are high-credibility.")
    
    # Add confidence information
    confidence_level = "high" if credibility_score > 0.7 or credibility_score < 0.3 else "moderate"
    explanation_parts.append(f"Confidence level: {confidence_level} "
                           f"(score: {credibility_score:.2f}).")
    
    return " ".join(explanation_parts)


def _extract_sources(context_data: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Extract and format source references from context data.
    
    Args:
        context_data (List[Dict[str, Any]]): Context data from vector database
        
    Returns:
        List[Dict[str, str]]: Formatted source references
    """
    sources = []
    
    for context in context_data:
        source = {
            "title": context.get("source_title", "Unknown Source"),
            "url": context.get("source_url", ""),
            "credibility": context.get("credibility_rating", "unknown"),
            "relevance": f"{context.get('similarity_score', 0.0):.2f}"
        }
        sources.append(source)
    
    # Sort by relevance (similarity score) descending
    sources.sort(key=lambda x: float(x["relevance"]), reverse=True)
    
    return sources