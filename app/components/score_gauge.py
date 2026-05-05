import plotly.graph_objects as go
import streamlit as st
from app.styles.theme import SCORE_COLORS, COLORS
import streamlit.components.v1 as components


def render_score_gauge(score: int, band: str, risk_level: str, previous_score: int = None):
    """
    Renders an animated credit score gauge with counter animation.
    
    Args:
        score: Current credit score (300-850)
        band: Score band (Poor/Fair/Good/Excellent)
        risk_level: Risk level description
        previous_score: Previous score for comparison (optional)
    """
    band_color = SCORE_COLORS.get(band, COLORS["accent"])
    
    # Calculate score change if previous score provided
    score_change = None
    change_html = ""
    if previous_score and previous_score != score:
        score_change = score - previous_score
        change_color = COLORS["success"] if score_change > 0 else COLORS["danger"]
        change_icon = "▲" if score_change > 0 else "▼"
        change_html = f"""
        <div style="margin-top: 0.5rem; font-size: 0.85rem;">
            <span style="color: {change_color}; font-weight: 600;">
                {change_icon} {abs(score_change)} points
            </span>
            <span style="color: #6B7280;"> since last check</span>
        </div>
        """
    
    # Create animated HTML component with enhanced features
    animated_html = f"""
    <div style="text-align: center; padding: 0.5rem;">
        <div style="position: relative; display: inline-block; width: 100%; max-width: 320px; margin: 0 auto;">
            <canvas id="scoreCanvas" width="320" height="320" style="width: 100%; height: auto; cursor: pointer;"></canvas>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                <div id="scoreValue" style="font-size: 3rem; font-weight: bold; color: {band_color}; font-family: 'Inter', sans-serif; transition: all 0.3s ease;">0</div>
                <div style="font-size: 0.75rem; color: #6B7280;">out of 850</div>
                {change_html}
            </div>
        </div>
    </div>
    
    <style>
        canvas:hover {{
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.1));
            transition: filter 0.3s ease;
        }}
        
        @keyframes glowPulse {{
            0%, 100% {{ filter: drop-shadow(0 0 0px {band_color}); }}
            50% {{ filter: drop-shadow(0 0 8px {band_color}); }}
        }}
        
        canvas.score-animated {{
            animation: glowPulse 2s ease-in-out;
        }}
    </style>
    
    <script>
    (function() {{
        const targetScore = {score};
        const maxScore = 850;
        const minScore = 300;
        const duration = 1500;
        
        const canvas = document.getElementById('scoreCanvas');
        const ctx = canvas.getContext('2d');
        const scoreDisplay = document.getElementById('scoreValue');
        
        // Set canvas dimensions
        const size = 320;
        canvas.width = size;
        canvas.height = size;
        
        const centerX = size / 2;
        const centerY = size / 2;
        const radius = 130;
        const startAngle = -0.5 * Math.PI;
        
        let startTime = null;
        let startScore = 300;
        let animationComplete = false;
        
        function easeOutCubic(t) {{
            return 1 - Math.pow(1 - t, 3);
        }}
        
        function formatScore(scoreValue) {{
            return Math.round(scoreValue).toString();
        }}
        
        function getScoreColor(scoreValue) {{
            if (scoreValue >= 750) return '{COLORS.get("excellent", "#00C2A8")}';
            if (scoreValue >= 700) return '{COLORS.get("good", "#4CAF50")}';
            if (scoreValue >= 580) return '{COLORS.get("fair", "#FF9800")}';
            return '{COLORS.get("poor", "#F44336")}';
        }}
        
        function drawGauge(currentScore) {{
            ctx.clearRect(0, 0, size, size);
            
            // Draw background gradient
            const gradient = ctx.createLinearGradient(0, 0, size, size);
            gradient.addColorStop(0, '#f8f9fa');
            gradient.addColorStop(1, '#e9ecef');
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            ctx.fillStyle = gradient;
            ctx.fill();
            
            // Draw background circle (track)
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            ctx.strokeStyle = '#E5E7EB';
            ctx.lineWidth = 20;
            ctx.stroke();
            
            // Draw progress circle with gradient
            const progress = (currentScore - minScore) / (maxScore - minScore);
            const clampedProgress = Math.max(0, Math.min(1, progress));
            const endAngle = startAngle + (2 * Math.PI * clampedProgress);
            
            // Create gradient for the progress arc
            const progressGradient = ctx.createLinearGradient(
                centerX - radius, centerY - radius,
                centerX + radius, centerY + radius
            );
            const currentColor = getScoreColor(currentScore);
            progressGradient.addColorStop(0, currentColor);
            progressGradient.addColorStop(1, currentColor + 'cc');
            
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, startAngle, endAngle);
            ctx.strokeStyle = progressGradient;
            ctx.lineWidth = 20;
            ctx.lineCap = 'round';
            ctx.stroke();
            
            // Draw tick marks at thresholds with labels
            const thresholds = [
                {{value: 450, label: 'Fair', color: '#FF9800'}},
                {{value: 580, label: 'Good', color: '#4CAF50'}},
                {{value: 700, label: 'Great', color: '#2196F3'}},
                {{value: 750, label: 'Excellent', color: '#00C2A8'}}
            ];
            
            thresholds.forEach(threshold => {{
                const angle = startAngle + (2 * Math.PI * ((threshold.value - minScore) / (maxScore - minScore)));
                const x1 = centerX + (radius - 12) * Math.cos(angle);
                const y1 = centerY + (radius - 12) * Math.sin(angle);
                const x2 = centerX + (radius + 8) * Math.cos(angle);
                const y2 = centerY + (radius + 8) * Math.sin(angle);
                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.strokeStyle = '#9CA3AF';
                ctx.lineWidth = 2;
                ctx.stroke();
                
                // Add small label
                const labelX = centerX + (radius + 20) * Math.cos(angle);
                const labelY = centerY + (radius + 20) * Math.sin(angle);
                ctx.font = '10px Inter, sans-serif';
                ctx.fillStyle = '#6B7280';
                ctx.fillText(threshold.label, labelX - 12, labelY - 5);
            }});
            
            // Draw center dot
            ctx.beginPath();
            ctx.arc(centerX, centerY, 12, 0, 2 * Math.PI);
            ctx.fillStyle = '#FFFFFF';
            ctx.fill();
            ctx.shadowBlur = 0;
            ctx.beginPath();
            ctx.arc(centerX, centerY, 8, 0, 2 * Math.PI);
            ctx.fillStyle = currentColor;
            ctx.fill();
        }}
        
        function animate(timestamp) {{
            if (!startTime) startTime = timestamp;
            const elapsed = timestamp - startTime;
            let progress = Math.min(1, elapsed / duration);
            const easedProgress = easeOutCubic(progress);
            
            const currentScore = Math.round(startScore + (targetScore - startScore) * easedProgress);
            scoreDisplay.textContent = formatScore(currentScore);
            drawGauge(currentScore);
            
            if (progress < 1) {{
                requestAnimationFrame(animate);
            }} else {{
                animationComplete = true;
                canvas.classList.add('score-animated');
                setTimeout(() => {{
                    canvas.classList.remove('score-animated');
                }}, 2000);
            }}
        }}
        
        requestAnimationFrame(animate);
        
        // Add click handler to replay animation
        canvas.addEventListener('click', () => {{
            if (animationComplete) {{
                startTime = null;
                startScore = 300;
                animationComplete = false;
                requestAnimationFrame(animate);
                
                // Emit custom event for potential parent listeners
                const event = new CustomEvent('gaugeReplayed', {{ detail: {{ score: targetScore }} }});
                canvas.dispatchEvent(event);
            }}
        }});
        
        // Add tooltip on hover
        canvas.title = 'Click to replay animation | Score: {score} - {band}';
    }})();
    </script>
    """
    
    # Show the animated gauge
    components.html(animated_html, height=360)
    
    # Enhanced band label with tooltip and hover effect
    badge_class = f"badge-{band.lower()}"
    pill_bg = {
        "Poor":      COLORS.get("danger_light", "#FFEBEE"),
        "Fair":      COLORS.get("warning_light", "#FFF3E0"),
        "Good":      COLORS.get("success_light", "#E8F5E9"),
        "Excellent": COLORS.get("teal_light", "#E0F2F1"),
    }.get(band, "#F3F4F6")
    
    # Band descriptions for tooltips
    band_descriptions = {
        "Poor": "Score needs significant improvement. Focus on building positive credit history.",
        "Fair": "Below average. Work on reducing debt and making timely payments.",
        "Good": "Above average. You qualify for most financial products.",
        "Excellent": "Top tier! You get the best interest rates and terms."
    }
    
    st.markdown(
        f"""
    <style>
        .score-badge-wrapper {{
            display: inline-block;
            transition: transform 0.2s ease;
            cursor: help;
        }}
        .score-badge-wrapper:hover {{
            transform: translateY(-2px);
        }}
        .score-badge {{
            display: inline-block;
            padding: 0.35rem 1rem;
            border-radius: 25px;
            font-weight: 600;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
            transition: all 0.2s ease;
        }}
        .score-badge:hover {{
            transform: scale(1.02);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .risk-level {{
            transition: color 0.2s ease;
        }}
        .risk-level:hover {{
            color: {band_color} !important;
        }}
    </style>
    
    <div style="text-align:center; margin-top:-0.5rem; margin-bottom:0.5rem;">
        <div class="score-badge-wrapper" title="{band_descriptions.get(band, '')}">
            <span class="score-badge" style="background:{pill_bg}; color:{band_color};">
                🏆 {band.upper()}
            </span>
        </div>
        <div style="color:#6B7280; font-size:0.82rem; margin-top:0.6rem;">
            Risk Level: 
            <strong class="risk-level" style="color:{band_color};">{risk_level}</strong>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    # Add percentile information (optional)
    if score >= 750:
        st.caption("✨ You're in the top 10% of credit users!")
    elif score >= 700:
        st.caption("📈 You're above average! Keep up the good habits.")
    elif score >= 580:
        st.caption("💪 You're making progress. Focus on timely payments.")
    else:
        st.caption("🌱 Every journey starts somewhere. We're here to help you grow!")


def render_mini_score_gauge(score: int, band: str):
    """
    Compact version of the score gauge for sidebars or dashboards.
    """
    band_color = SCORE_COLORS.get(band, COLORS["accent"])
    
    mini_html = f"""
    <div style="text-align: center; padding: 0.25rem;">
        <canvas id="miniCanvas" width="120" height="120"></canvas>
        <div style="margin-top: 0.25rem;">
            <span style="font-size: 1.2rem; font-weight: bold; color: {band_color};">{score}</span>
            <span style="font-size: 0.7rem; color: #6B7280;">/850</span>
        </div>
    </div>
    
    <script>
    (function() {{
        const canvas = document.getElementById('miniCanvas');
        const ctx = canvas.getContext('2d');
        const size = 120;
        canvas.width = size;
        canvas.height = size;
        
        const centerX = size / 2;
        const centerY = size / 2;
        const radius = 50;
        const startAngle = -0.5 * Math.PI;
        const progress = ({score} - 300) / (850 - 300);
        const endAngle = startAngle + (2 * Math.PI * Math.min(1, Math.max(0, progress)));
        
        // Draw background
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        ctx.strokeStyle = '#E5E7EB';
        ctx.lineWidth = 8;
        ctx.stroke();
        
        // Draw progress
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.strokeStyle = '{band_color}';
        ctx.lineWidth = 8;
        ctx.lineCap = 'round';
        ctx.stroke();
    }})();
    </script>
    """
    
    components.html(mini_html, height=140)