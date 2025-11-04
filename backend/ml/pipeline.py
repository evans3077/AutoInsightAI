import logging
from typing import Dict, Any
import numpy as np

class SimpleVideoAnalysis:
    def analyze_video_content(self, video_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simplified analysis pipeline - no external model server needed
        """
        try:
            # Mock analysis for MVP
            title = metadata.get("title", "")
            filename = metadata.get("filename", "")
            
            # Basic text analysis
            title_quality = self.analyze_title(title)
            content_potential = self.estimate_content_potential(filename, title)
            
            insights = {
                "engagement_score": content_potential,
                "predictions": {
                    "estimated_ctr": content_potential * 0.08,
                    "retention_estimate": content_potential * 0.75,
                },
                "recommendations": self.generate_basic_recommendations(title, content_potential),
                "analysis": {
                    "title_analysis": title_quality,
                    "content_type": self.detect_content_type(title)
                }
            }
            
            return insights
            
        except Exception as e:
            logging.error(f"Analysis failed: {e}")
            return {"error": str(e), "engagement_score": 0.5}
    
    def analyze_title(self, title: str) -> Dict[str, Any]:
        """Basic title analysis"""
        words = title.split()
        return {
            "word_count": len(words),
            "has_question": "?" in title,
            "has_numbers": any(char.isdigit() for char in title),
            "length_score": min(len(title) / 50.0, 1.0)  # Normalize
        }
    
    def estimate_content_potential(self, filename: str, title: str) -> float:
        """Simple content potential estimation"""
        score = 0.5  # Base score
        
        # Boost for certain keywords
        boost_keywords = ['tutorial', 'how to', 'review', 'guide', 'tips']
        if any(keyword in title.lower() for keyword in boost_keywords):
            score += 0.2
        
        # Boost for reasonable title length
        title_words = len(title.split())
        if 5 <= title_words <= 15:
            score += 0.2
        
        return min(score, 1.0)
    
    def generate_basic_recommendations(self, title: str, score: float) -> list:
        """Generate basic recommendations"""
        recommendations = []
        
        if len(title.split()) < 5:
            recommendations.append("Consider a more descriptive title (5-15 words ideal)")
        
        if score < 0.6:
            recommendations.append("Add keywords like 'tutorial', 'guide', or 'review' to improve discoverability")
        
        if "?" not in title:
            recommendations.append("Try using questions in your title to spark curiosity")
        
        return recommendations
    
    def detect_content_type(self, title: str) -> str:
        """Detect content type from title"""
        title_lower = title.lower()
        if any(word in title_lower for word in ['tutorial', 'how to', 'guide']):
            return "Educational"
        elif any(word in title_lower for word in ['review', 'unboxing']):
            return "Review"
        elif any(word in title_lower for word in ['vlog', 'day in life']):
            return "Vlog"
        else:
            return "General"

# Global instance
analyzer = SimpleVideoAnalysis()

def analyze_video_content(video_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    return analyzer.analyze_video_content(video_path, metadata)