import plotly.graph_objects as go
import streamlit as st
from app.styles.theme import SCORE_COLORS, COLORS
import streamlit.components.v1 as components


def render_score_gauge(score: int, band: str, risk_level: str):
    """
    Renders an animated credit score gauge with counter animation.
    """
    band_color = SCORE_COLORS.get(band, COLORS["accent"])
    
    # Create animated HTML component with both counter and gauge
    animated_html = f"""
    <div style="text-align: center; padding: 0.5rem;">
        <div style="position: relative; display: inline-block; width: 100%; max-width: 280px;">
            <canvas id="scoreCanvas" width="280" height="280" style="width: 100%; height: auto;"></canvas>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                <div id="scoreValue" style="font-size: 2.8rem; font-weight: bold; color: {band_color}; font-family: 'Inter', sans-serif;">0</div>
                <div style="font-size: 0.75rem; color: #6B7280;">out of 850</div>
            </div>
        </div>
    </div>
    
    <script>
    (function() {{
        const targetScore = {score};
        const maxScore = 850;
        const duration = 1500;
        
        const canvas = document.getElementById('scoreCanvas');
        const ctx = canvas.getContext('2d');
        const scoreDisplay = document.getElementById('scoreValue');
        
        // Set canvas dimensions
        const size = 280;
        canvas.width = size;
        canvas.height = size;
        
        const centerX = size / 2;
        const centerY = size / 2;
        const radius = 110;
        const startAngle = -0.5 * Math.PI;
        
        let startTime = null;
        let startScore = 300;
        
        function easeOutCubic(t) {{
            return 1 - Math.pow(1 - t, 3);
        }}
        
        function drawGauge(currentScore) {{
            ctx.clearRect(0, 0, size, size);
            
            // Draw background circle
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            ctx.strokeStyle = '#E8E8E8';
            ctx.lineWidth = 18;
            ctx.stroke();
            
            // Draw progress circle
            const progress = (currentScore - 300) / (maxScore - 300);
            const clampedProgress = Math.max(0, Math.min(1, progress));
            const endAngle = startAngle + (2 * Math.PI * clampedProgress);
            
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, startAngle, endAngle);
            ctx.strokeStyle = '{band_color}';
            ctx.lineWidth = 18;
            ctx.lineCap = 'round';
            ctx.stroke();
            
            // Draw tick marks at thresholds
            const thresholds = [450, 580, 700];
            thresholds.forEach(threshold => {{
                const angle = startAngle + (2 * Math.PI * ((threshold - 300) / (maxScore - 300)));
                const x1 = centerX + (radius - 5) * Math.cos(angle);
                const y1 = centerY + (radius - 5) * Math.sin(angle);
                const x2 = centerX + (radius + 5) * Math.cos(angle);
                const y2 = centerY + (radius + 5) * Math.sin(angle);
                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.strokeStyle = '#999';
                ctx.lineWidth = 2;
                ctx.stroke();
            }});
        }}
        
        function animate(timestamp) {{
            if (!startTime) startTime = timestamp;
            const elapsed = timestamp - startTime;
            let progress = Math.min(1, elapsed / duration);
            const easedProgress = easeOutCubic(progress);
            
            const currentScore = Math.round(startScore + (targetScore - startScore) * easedProgress);
            scoreDisplay.textContent = currentScore;
            drawGauge(currentScore);
            
            if (progress < 1) {{
                requestAnimationFrame(animate);
            }}
        }}
        
        requestAnimationFrame(animate);
    }})();
    </script>
    """
    
    # Show the animated gauge
    components.html(animated_html, height=320)
    
    # Band label below chart
    badge_class = f"badge-{band.lower()}"
    pill_bg = {
        "Poor":      COLORS.get("danger_light", "#FFEBEE"),
        "Fair":      COLORS.get("warning_light", "#FFF3E0"),
        "Good":      COLORS.get("success_light", "#E8F5E9"),
        "Excellent": COLORS.get("teal_light", "#E0F2F1"),
    }.get(band, "#F3F4F6")
    
    st.markdown(
        f"""
    <div style="text-align:center; margin-top:-1rem; margin-bottom:1rem;">
        <span class="score-badge {badge_class}" style="background:{pill_bg}; color:{band_color}; padding:0.25rem 0.75rem; border-radius:20px; font-weight:500;">{band.upper()}</span>
        <div style="color:#6B7280; font-size:0.82rem; margin-top:0.4rem;">
            Risk Level: <strong>{risk_level}</strong>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )