import streamlit as st
import streamlit.components.v1 as components
import re
import html
import base64
import json
import graphviz
import requests
from datetime import datetime
from functools import lru_cache
import hashlib

# --- Page Configuration ---
st.set_page_config(
    page_title="CloudDMate Architecture",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Colorful UI with Better Text Visibility ---
st.markdown("""
<style>
    /* Main container styling with subtle gradient background */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.03) 0%, rgba(118, 75, 162, 0.03) 25%, rgba(240, 147, 251, 0.03) 50%, rgba(79, 172, 254, 0.03) 75%, rgba(0, 242, 254, 0.03) 100%);
    }
    
    /* Ensure all text is readable */
    .main * {
        color: #1f2937 !important;
    }
    
    /* Sidebar styling with colorful gradient but readable text */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stTextInput label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stCaption {
        color: white !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="stSidebar"] .stSelectbox>div>div,
    [data-testid="stSidebar"] .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #1f2937 !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
    }
    
    [data-testid="stSidebar"] .stCheckbox label {
        color: white !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="stSidebar"] .stInfo {
        background: rgba(255, 255, 255, 0.25) !important;
        border-left: 4px solid white !important;
        color: white !important;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .stSuccess {
        background: rgba(16, 185, 129, 0.4) !important;
        border-left: 4px solid #10b981 !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stWarning {
        background: rgba(245, 158, 11, 0.4) !important;
        border-left: 4px solid #f59e0b !important;
        color: white !important;
    }
    
    /* Column spacing */
    .stColumn {
        padding: 0 10px;
    }
    
    /* Colorful headings with solid colors for better visibility */
    h1 {
        color: #667eea !important;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-weight: bold;
        text-shadow: 0 1px 2px rgba(102, 126, 234, 0.2);
    }
    
    h2 {
        color: #764ba2 !important;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 1px 2px rgba(118, 75, 162, 0.2);
    }
    
    h3 {
        color: #4facfe !important;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 1px 2px rgba(79, 172, 254, 0.2);
    }
    
    h4 {
        color: #667eea !important;
        font-weight: 600;
    }
    
    /* Ensure all paragraph text is readable */
    p {
        color: #1f2937 !important;
    }
    
    /* Colorful button styling */
    .stDownloadButton>button,
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
        font-weight: 600;
    }
    
    .stDownloadButton>button:hover,
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Colorful metric cards with readable text */
    [data-testid="stMetricContainer"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: #667eea !important;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: #764ba2 !important;
        font-weight: 600;
    }
    
    /* Colorful tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(90deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
    }
    
    /* Colorful input area styling with white background */
    textarea {
        border-radius: 8px;
        border: 2px solid #667eea;
        background: white !important;
        color: #1f2937 !important;
    }
    
    textarea:focus {
        border-color: #764ba2;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        background: white !important;
    }
    
    /* Colorful info boxes with readable text */
    .stInfo {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%);
        border-left: 4px solid #4facfe;
        border-radius: 8px;
        padding: 1rem;
        color: #1f2937 !important;
    }
    
    .stInfo * {
        color: #1f2937 !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        border-left: 4px solid #10b981;
        color: #065f46 !important;
    }
    
    .stSuccess * {
        color: #065f46 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
        border-left: 4px solid #f59e0b;
        color: #92400e !important;
    }
    
    .stWarning * {
        color: #92400e !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
        border-left: 4px solid #ef4444;
        color: #991b1b !important;
    }
    
    .stError * {
        color: #991b1b !important;
    }
    
    /* Colorful selectbox and text input with white background */
    .stSelectbox>div>div,
    .stTextInput>div>div>input {
        background: white !important;
        border: 2px solid #667eea;
        border-radius: 8px;
        color: #1f2937 !important;
    }
    
    .stSelectbox>div>div:focus,
    .stTextInput>div>div>input:focus {
        border-color: #764ba2;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        background: white !important;
    }
    
    /* Colorful checkbox */
    .stCheckbox label {
        color: #667eea !important;
        font-weight: 600;
    }
    
    /* Divider spacing with color */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
    }
    
    /* Colorful radio buttons */
    .stRadio>div {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    .stRadio label {
        color: #1f2937 !important;
    }
    
    /* Colorful expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 8px;
        color: #667eea !important;
        font-weight: 600;
    }
    
    /* Colorful file uploader */
    .stFileUploader>div {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%);
        border: 2px dashed #4facfe;
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Main content background - subtle */
    .main {
        background: white;
    }
    
    /* Code blocks */
    code {
        background: rgba(102, 126, 234, 0.1) !important;
        color: #667eea !important;
        padding: 2px 6px;
        border-radius: 4px;
    }
    
    /* Caption text */
    .stCaption {
        color: #6b7280 !important;
    }
    
    /* JSON display */
    .stJson {
        background: rgba(102, 126, 234, 0.05) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 8px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Enhanced Icon Logic ---
def add_icons(label):
    """Injects icons based on keywords to make diagrams more visual and creative."""
    l = label.lower()
    prefix = ""
    if any(x in l for x in ["user", "actor", "client", "customer"]): prefix = "👤 "
    elif any(x in l for x in ["db", "data", "sql", "store", "oracle", "database"]): prefix = "🛢️ "
    elif any(x in l for x in ["cloud", "aws", "azure", "gcp"]): prefix = "☁️ "
    elif any(x in l for x in ["api", "rest", "json", "endpoint", "service"]): prefix = "🔌 "
    elif any(x in l for x in ["lock", "auth", "login", "security", "token"]): prefix = "🔒 "
    elif any(x in l for x in ["email", "message", "notification", "alert"]): prefix = "📧 "
    elif any(x in l for x in ["error", "fail", "404", "500", "exception"]): prefix = "⚠️ "
    elif any(x in l for x in ["settings", "config", "setup", "configuration"]): prefix = "⚙️ "
    elif any(x in l for x in ["file", "upload", "excel", "csv", "document"]): prefix = "📄 "
    elif any(x in l for x in ["check", "validate", "success", "ok", "verified"]): prefix = "✅ "
    elif any(x in l for x in ["web", "site", "dashboard", "ui", "interface"]): prefix = "🖥️ "
    elif any(x in l for x in ["mobile", "app", "phone", "ios", "android"]): prefix = "📱 "
    elif any(x in l for x in ["server", "host", "machine", "vm"]): prefix = "🖥️ "
    elif any(x in l for x in ["network", "router", "switch", "gateway"]): prefix = "🌐 "
    elif any(x in l for x in ["queue", "message", "broker", "kafka", "rabbit"]): prefix = "📬 "
    elif any(x in l for x in ["cache", "redis", "memcached"]): prefix = "⚡ "
    elif any(x in l for x in ["search", "elastic", "lucene"]): prefix = "🔍 "
    elif any(x in l for x in ["payment", "transaction", "money", "billing"]): prefix = "💳 "
    elif any(x in l for x in ["analytics", "report", "metrics", "stats"]): prefix = "📊 "
    elif any(x in l for x in ["monitor", "log", "trace", "debug"]): prefix = "📈 "
    elif any(x in l for x in ["deploy", "ci", "cd", "pipeline", "build"]): prefix = "🚀 "
    elif any(x in l for x in ["test", "qa", "quality"]): prefix = "🧪 "
    elif any(x in l for x in ["start", "begin", "init"]): prefix = "▶️ "
    elif any(x in l for x in ["end", "finish", "complete", "done"]): prefix = "🏁 "
    elif any(x in l for x in ["load", "balance", "distribute"]): prefix = "⚖️ "
    elif any(x in l for x in ["sync", "replicate", "copy"]): prefix = "🔄 "
    elif any(x in l for x in ["delete", "remove", "drop"]): prefix = "🗑️ "
    elif any(x in l for x in ["add", "create", "insert", "new"]): prefix = "➕ "
    elif any(x in l for x in ["update", "modify", "edit", "change"]): prefix = "✏️ "
    elif any(x in l for x in ["read", "get", "fetch", "retrieve"]): prefix = "📖 "
    elif any(x in l for x in ["write", "post", "put", "save"]): prefix = "✍️ "
    
    return f"{prefix}{label}"

# --- Advanced Theming System ---

THEMES = {
    "Professional (Blue)": {
        "bgcolor": "#ffffff",
        "edge_color": "#555555",
        "font": "Helvetica",
        "default": {"shape": "box", "style": "rounded,filled", "fill": "#e6f3ff", "border": "#336699", "text": "#000000"},
        "types": {
            "database": {"shape": "cylinder", "fill": "#fff3cd", "border": "#856404", "text": "#000000"},
            "api": {"shape": "component", "fill": "#d1e7dd", "border": "#0f5132", "text": "#000000"},
            "error": {"shape": "box", "style": "filled,dashed", "fill": "#f8d7da", "border": "#842029", "text": "#000000"},
            "ui": {"shape": "rect", "fill": "#cff4fc", "border": "#055160", "text": "#000000"},
            "actor": {"shape": "ellipse", "fill": "#e2e3e5", "border": "#383d41", "text": "#000000"}
        }
    },
    "Whiteboard Sketch": {
        "bgcolor": "#ffffff",
        "edge_color": "#333333",
        "font": "Comic Sans MS",
        "default": {"shape": "box", "style": "dashed", "fill": "#ffffff", "border": "#333333", "text": "#333333"},
        "types": {
            "database": {"shape": "cylinder", "fill": "#ffffff", "border": "#333333", "text": "#333333"},
            "api": {"shape": "component", "fill": "#ffffff", "border": "#333333", "text": "#333333"},
            "error": {"shape": "box", "style": "dotted", "fill": "#ffffff", "border": "#ff0000", "text": "#ff0000"},
            "ui": {"shape": "rect", "fill": "#ffffff", "border": "#0000ff", "text": "#0000ff"},
            "actor": {"shape": "ellipse", "fill": "#ffffff", "border": "#333333", "text": "#333333"}
        }
    },
    "Neon Cyberpunk": {
        "bgcolor": "#0b0f19",
        "edge_color": "#00f3ff",
        "font": "Courier",
        "default": {"shape": "polygon", "style": "filled", "fill": "#1a1f2e", "border": "#00f3ff", "text": "#e0e0e0"},
        "types": {
            "database": {"shape": "cylinder", "fill": "#2d1b2e", "border": "#ff0055", "text": "#ff0055"},
            "api": {"shape": "component", "fill": "#0d2b2a", "border": "#00ff99", "text": "#00ff99"},
            "error": {"shape": "box", "style": "dashed", "fill": "#2a0e0e", "border": "#ff3333", "text": "#ff3333"},
            "ui": {"shape": "parallelogram", "fill": "#1a2a3a", "border": "#00aaff", "text": "#00aaff"},
            "actor": {"shape": "diamond", "fill": "#222222", "border": "#ffff00", "text": "#ffff00"}
        }
    },
    "Blueprint": {
        "bgcolor": "#1c3b70",
        "edge_color": "#ffffff",
        "font": "Consolas",
        "default": {"shape": "box", "style": "filled", "fill": "#1c3b70", "border": "#ffffff", "text": "#ffffff"},
        "types": {
            "database": {"shape": "cylinder", "fill": "#1c3b70", "border": "#ffffff", "text": "#ffffff"},
            "api": {"shape": "component", "fill": "#1c3b70", "border": "#ffffff", "text": "#ffffff"},
            "error": {"shape": "box", "style": "dashed", "fill": "#1c3b70", "border": "#ff6b6b", "text": "#ff6b6b"},
            "ui": {"shape": "rect", "fill": "#1c3b70", "border": "#ffffff", "text": "#ffffff"},
            "actor": {"shape": "ellipse", "fill": "#1c3b70", "border": "#ffffff", "text": "#ffffff"}
        }
    },
    "Minimalist": {
        "bgcolor": "#fafafa",
        "edge_color": "#cccccc",
        "font": "Arial",
        "default": {"shape": "box", "style": "rounded", "fill": "#ffffff", "border": "#333333", "text": "#333333"},
        "types": {
            "database": {"shape": "cylinder", "fill": "#ffffff", "border": "#666666", "text": "#333333"},
            "api": {"shape": "component", "fill": "#ffffff", "border": "#666666", "text": "#333333"},
            "error": {"shape": "box", "style": "dashed", "fill": "#ffffff", "border": "#cc0000", "text": "#cc0000"},
            "ui": {"shape": "rect", "fill": "#ffffff", "border": "#666666", "text": "#333333"},
            "actor": {"shape": "ellipse", "fill": "#ffffff", "border": "#666666", "text": "#333333"}
        }
    },
    "Vibrant": {
        "bgcolor": "#ffffff",
        "edge_color": "#333333",
        "font": "Verdana",
        "default": {"shape": "box", "style": "rounded,filled", "fill": "#e8f4f8", "border": "#2c5aa0", "text": "#1a1a1a"},
        "types": {
            "database": {"shape": "cylinder", "fill": "#fff4e6", "border": "#ff8c00", "text": "#1a1a1a"},
            "api": {"shape": "component", "fill": "#e8f5e9", "border": "#4caf50", "text": "#1a1a1a"},
            "error": {"shape": "box", "style": "filled,dashed", "fill": "#ffebee", "border": "#f44336", "text": "#1a1a1a"},
            "ui": {"shape": "rect", "fill": "#f3e5f5", "border": "#9c27b0", "text": "#1a1a1a"},
            "actor": {"shape": "ellipse", "fill": "#e1f5fe", "border": "#03a9f4", "text": "#1a1a1a"}
        }
    }
}

def get_node_type(label):
    label_lower = label.lower()
    if any(x in label_lower for x in ["db", "database", "store", "storage", "sql", "oracle"]): return "database"
    elif any(x in label_lower for x in ["api", "post", "get", "endpoint", "request"]): return "api"
    elif any(x in label_lower for x in ["error", "failure", "401", "403", "500"]): return "error"
    elif any(x in label_lower for x in ["user", "customer", "actor"]): return "actor"
    elif any(x in label_lower for x in ["dashboard", "ui", "screen", "dialog", "wizard", "mode"]): return "ui"
    return "default"

def get_graphviz_style(label, theme_name, visualization_mode="flow"):
    theme = THEMES[theme_name]
    node_type = get_node_type(label)
    style_config = theme["types"].get(node_type, theme["default"])
    base_config = theme["default"].copy()
    base_config.update(style_config)
    s = base_config
    
    # Enhanced styling based on visualization mode
    if visualization_mode == "mindmap":
        # Use more organic shapes for mind maps
        shape = "ellipse" if node_type == "default" else s["shape"]
        style = f'style="{s.get("style", "filled")},rounded"'
    elif visualization_mode == "sequence":
        # Use boxes for sequence diagrams
        shape = "box"
        style = f'style="{s.get("style", "filled")},rounded"'
    elif visualization_mode == "network":
        # Use varied shapes for network diagrams
        shape = s["shape"]
        style = f'style="{s.get("style", "filled")},rounded"'
    else:
        shape = s["shape"]
        style = f'style="{s.get("style", "filled")}"'
    
    return f'shape="{shape}", {style}, fillcolor="{s["fill"]}", color="{s["border"]}", fontcolor="{s["text"]}"'

def get_drawio_style(label):
    node_type = get_node_type(label)
    base_style = "rounded=1;whiteSpace=wrap;html=1;absoluteArcSize=1;arcSize=14;strokeWidth=2;"
    if node_type == "database": return "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;"
    elif node_type == "api": return "shape=component;align=left;spacingLeft=36;fillColor=#d5e8d4;strokeColor=#82b366;"
    elif node_type == "error": return "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;dashed=1;"
    elif node_type == "actor": return "shape=ellipse;fillColor=#dae8fc;strokeColor=#6c8ebf;"
    elif node_type == "ui": return "rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;"
    return base_style + "fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;"

def parse_diagram_data(text):
    """Enhanced parser with edge label support."""
    lines = text.split('\n')
    clusters = [] 
    nodes = {}    
    edges = []  # Now stores (src, dst, label) tuples
    current_cluster = None
    cluster_counter = 0
    last_node_id_of_prev_line = None
    connect_next_line = False
    arrow_split_re = r'\s*(?:→|->|=>)\s*'
    edge_label_re = r'\[([^\]]+)\]'  # Matches [label] on edges
    
    for line in lines:
        line = line.strip()
        if not line: continue
            
        if line.startswith('#'):
            title = line.lstrip('#').strip()
            current_cluster = {'id': f'cluster_{cluster_counter}', 'title': title, 'nodes': set()}
            clusters.append(current_cluster)
            cluster_counter += 1
            last_node_id_of_prev_line = None 
            connect_next_line = False
            continue

        clean_line_check = line.replace(" ", "")
        if clean_line_check in ['↓', 'v', '|', '||']:
            connect_next_line = True
            continue
            
        # Extract edge labels from the line
        edge_labels = {}
        for match in re.finditer(edge_label_re, line):
            label_text = match.group(1)
            # Find the arrow before this label
            pos = match.start()
            # Simple heuristic: label belongs to the arrow before it
            edge_labels[pos] = label_text
            line = line[:match.start()] + line[match.end():]
            
        parts = re.split(arrow_split_re, line)
        row_node_ids = []
        
        for idx, part in enumerate(parts):
            label = part.strip().replace("┌", "").replace("┐", "").replace("└", "").replace("┘", "").replace("│", "")
            if label.endswith("↓"):
                label = label[:-1].strip()
                connect_next_line = True
            if label.startswith("↓"):
                label = label[1:].strip()
                connect_next_line = True
            if not label: continue
                
            nid = re.sub(r'\W+', '_', label).strip('_')
            if not nid: nid = f"node_{abs(hash(label))}"
            
            # Add Icons to Label
            nodes[nid] = add_icons(label)
            row_node_ids.append(nid)
            
            if current_cluster:
                current_cluster['nodes'].add(nid)

        if not row_node_ids: continue

        if connect_next_line and last_node_id_of_prev_line:
            # Check for edge label
            edge_label = edge_labels.get(0, "") if edge_labels else ""
            edges.append((last_node_id_of_prev_line, row_node_ids[0], edge_label))
            connect_next_line = False
        
        for i in range(len(row_node_ids) - 1):
            # Check for edge label between nodes
            edge_label = edge_labels.get(i, "") if edge_labels else ""
            edges.append((row_node_ids[i], row_node_ids[i+1], edge_label))
            
        last_node_id_of_prev_line = row_node_ids[-1]

    return nodes, edges, clusters

def generate_dot_code(nodes, edges, clusters, theme_name, layout_engine="dot", splines="ortho", visualization_mode="flow", collapsed_clusters=None):
    """
    Generate Graphviz DOT code with enhanced visualization modes.
    """
    if collapsed_clusters is None:
        collapsed_clusters = set()
    
    theme = THEMES[theme_name]
    
    engine_map = {
        "Hierarchy (Waterfall)": "dot",
        "Organic (Force)": "neato",
        "Circular (Ring)": "circo",
        "Radial (Star)": "twopi",
        "Freeform": "fdp"
    }
    engine = engine_map.get(layout_engine, "dot")
    
    # Adjust layout based on visualization mode
    if visualization_mode == "sequence":
        rankdir_str = 'rankdir=LR;'
        engine = "dot"
    elif visualization_mode == "mindmap":
        engine = "twopi"
        rankdir_str = ''
    elif visualization_mode == "network":
        engine = "neato"
        rankdir_str = ''
    else:
        rankdir_str = 'rankdir=TB;' if engine == 'dot' else ''
    
    splines_val = 'curved' if engine in ['neato', 'fdp'] or visualization_mode == "mindmap" else splines
    
    # Enhanced styling based on visualization mode
    node_penwidth = 2.0 if visualization_mode in ["network", "mindmap"] else 1.5
    edge_penwidth = 1.5 if visualization_mode == "sequence" else 1.0
    
    dot = [
        'digraph G {',
        f'  layout={engine};',
        f'  {rankdir_str}',
        f'  bgcolor="transparent";',
        f'  splines={splines_val};',
        '  overlap=false;',  
        f'  nodesep={0.8 if visualization_mode == "mindmap" else 0.6};',
        f'  ranksep={1.2 if visualization_mode == "mindmap" else 0.8};',
        f'  node [fontname="{theme["font"]}", fontsize={12 if visualization_mode == "mindmap" else 10}, penwidth={node_penwidth}];',
        f'  edge [fontname="{theme["font"]}", fontsize=9, color="{theme["edge_color"]}", arrowsize=0.8, penwidth={edge_penwidth}];'
    ]
    
    def escape_label(s): return s.replace('"', '\\"')
    
    rendered_nodes = set()
    use_clusters = engine in ['dot', 'fdp'] and visualization_mode != "sequence"
    
    if use_clusters:
        for c in clusters:
            cluster_id = c["id"]
            is_collapsed = cluster_id in collapsed_clusters
            
            dot.append(f'  subgraph {cluster_id} {{')
            if is_collapsed:
                # Collapsed cluster - show only title
                dot.append(f'    label="{escape_label(c["title"])} [Collapsed]";')
                dot.append(f'    style="rounded,dashed,filled";')
                dot.append(f'    fillcolor="{theme["default"]["fill"]}";')
            else:
                dot.append(f'    label="{escape_label(c["title"])}";')
                dot.append(f'    style="rounded,dashed";')
                dot.append(f'    color="{theme["edge_color"]}";')
                dot.append(f'    fontcolor="{theme["edge_color"]}";')
            
            if not is_collapsed:
                for nid in c['nodes']:
                    if nid in nodes:
                        style = get_graphviz_style(nodes[nid], theme_name, visualization_mode)
                        dot.append(f'    {nid} [label="{escape_label(nodes[nid])}", {style}];')
                        rendered_nodes.add(nid)
            dot.append('  }')
            
    for nid, label in nodes.items():
        if not use_clusters or nid not in rendered_nodes:
            style = get_graphviz_style(label, theme_name, visualization_mode)
            dot.append(f'    {nid} [label="{escape_label(label)}", {style}];')
            
    for edge in edges:
        if len(edge) == 3 and edge[2]:  # Has label
            src, dst, label = edge
            edge_style = 'style="dashed"' if visualization_mode == "sequence" else ''
            dot.append(f'    {src} -> {dst} [label="{escape_label(label)}" {edge_style}];')
        else:
            src, dst = edge[0], edge[1]
            edge_style = 'style="dashed"' if visualization_mode == "sequence" else ''
            dot.append(f'    {src} -> {dst} [{edge_style}];')
        
    dot.append('}')
    return "\n".join(dot)

def generate_drawio_xml(nodes, edges, clusters):
    """Generate draw.io XML with proper layout and positioning."""
    import uuid
    
    # Create a better layout - arrange nodes in a grid or flow
    node_positions = {}
    node_width = 180
    node_height = 80
    spacing_x = 250
    spacing_y = 120
    start_x, start_y = 40, 40
    
    # Calculate positions for nodes
    node_list = list(nodes.items())
    cols = max(3, int(len(node_list) ** 0.5) + 1)
    
    for idx, (nid, label) in enumerate(node_list):
        row = idx // cols
        col = idx % cols
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        node_positions[nid] = (x, y)
    
    # Build XML
    diagram_id = str(uuid.uuid4())
    xml = [
        '<mxfile host="app.diagrams.net" modified="' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z') + '" agent="CloudDMate" version="21.0.0" type="device">',
        f'  <diagram id="{diagram_id}" name="Architecture">',
        '    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">',
        '      <root>',
        '        <mxCell id="0" />',
        '        <mxCell id="1" parent="0" />'
    ]
    
    # Add clusters as containers (swimlanes)
    cluster_cells = {}
    cluster_bounds = {}
    
    if clusters:
        for c_idx, c in enumerate(clusters):
            cluster_id = f"cluster_{c_idx}"
            cluster_cells[c["id"]] = cluster_id
            
            # Calculate cluster bounds based on nodes in cluster
            cluster_nodes = [nid for nid in c['nodes'] if nid in node_positions]
            if cluster_nodes:
                positions = [node_positions[nid] for nid in cluster_nodes]
                min_x = min(p[0] for p in positions) - 20
                min_y = min(p[1] for p in positions) - 40
                max_x = max(p[0] for p in positions) + node_width + 20
                max_y = max(p[1] for p in positions) + node_height + 20
                
                cluster_bounds[cluster_id] = (min_x, min_y, max_x - min_x, max_y - min_y)
                
                xml.append(f'        <mxCell id="{cluster_id}" value="{html.escape(c["title"])}" style="swimlane;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;startSize=30;fontStyle=1;fontSize=14;" vertex="1" parent="1">')
                xml.append(f'          <mxGeometry x="{min_x}" y="{min_y}" width="{max_x - min_x}" height="{max_y - min_y}" as="geometry" />')
                xml.append('        </mxCell>')
    
    # Add nodes
    for nid, label in nodes.items():
        style = get_drawio_style(label)
        x, y = node_positions.get(nid, (start_x, start_y))
        
        # Determine parent (cluster or root)
        parent = "1"
        for c in clusters:
            if nid in c['nodes'] and c["id"] in cluster_cells:
                parent = cluster_cells[c["id"]]
                # Adjust position relative to cluster (account for cluster header)
                if parent in cluster_bounds:
                    cluster_x, cluster_y, _, _ = cluster_bounds[parent]
                    x = x - cluster_x
                    y = y - cluster_y + 30  # Account for cluster header
                break
        
        xml.append(f'        <mxCell id="{nid}" value="{html.escape(label)}" style="{style}" vertex="1" parent="{parent}">')
        xml.append(f'          <mxGeometry x="{x}" y="{y}" width="{node_width}" height="{node_height}" as="geometry" />')
        xml.append('        </mxCell>')
    
    # Add edges
    edge_id = 10000
    for edge in edges:
        if len(edge) == 3 and edge[2]:  # Has label
            src, dst, label = edge
            edge_label = html.escape(label)
            xml.append(f'        <mxCell id="{edge_id}" value="{edge_label}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;" edge="1" parent="1" source="{src}" target="{dst}">')
        else:
            src, dst = edge[0], edge[1]
            xml.append(f'        <mxCell id="{edge_id}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;" edge="1" parent="1" source="{src}" target="{dst}">')
        xml.append('          <mxGeometry relative="1" as="geometry" />')
        xml.append('        </mxCell>')
        edge_id += 1
    
    xml.append('      </root></mxGraphModel></diagram></mxfile>')
    return "\n".join(xml)

def render_drawio_editor(xml_content):
    """Render fully functional draw.io editor with save/load capabilities."""
    # Use base64 encoding for safe XML transmission
    import base64
    xml_base64 = base64.b64encode(xml_content.encode('utf-8')).decode('utf-8')
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body, html {{ 
                margin: 0; 
                padding: 0; 
                height: 100vh; 
                width: 100%;
                overflow: hidden; 
                background: #f5f5f5; 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}
            #drawio-container {{
                width: 100%;
                height: 100%;
                position: relative;
                border: 1px solid #ddd;
                border-radius: 8px;
                overflow: hidden;
                background: white;
            }}
            #drawio-iframe {{ 
                width: 100%; 
                height: 100%; 
                border: none; 
                display: block;
            }}
            #controls {{
                position: absolute; 
                top: 10px; 
                right: 10px; 
                z-index: 1000;
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }}
            button {{ 
                background: #336699; 
                color: white; 
                border: none; 
                padding: 8px 16px; 
                border-radius: 4px; 
                cursor: pointer; 
                font-family: inherit;
                font-size: 13px;
                font-weight: 500;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                transition: all 0.2s;
            }}
            button:hover {{ 
                background: #2a5580;
                transform: translateY(-1px);
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }}
            button:active {{
                transform: translateY(0);
            }}
            button.secondary {{
                background: #6c757d;
            }}
            button.secondary:hover {{
                background: #5a6268;
            }}
            #status {{
                position: absolute;
                bottom: 10px;
                left: 10px;
                background: rgba(0,0,0,0.7);
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 1000;
                display: none;
            }}
            #status.show {{
                display: block;
                animation: fadeIn 0.3s;
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
        </style>
    </head>
    <body>
        <div id="drawio-container">
            <div id="status"></div>
            <div id="controls">
                <button onclick="loadDiagram()" title="Reload the diagram">🔄 Reload</button>
                <button onclick="exportDiagram()" title="Export diagram XML">💾 Export XML</button>
                <button onclick="exportPNG()" class="secondary" title="Export as PNG">📷 Export PNG</button>
            </div>
            <iframe 
                id="drawio-iframe" 
                src="https://embed.diagrams.net/?embed=1&ui=min&spin=1&proto=json&configure=1&grid=1&toolbar=yes"
                allowfullscreen
            ></iframe>
        </div>
        <script>
            const iframe = document.getElementById('drawio-iframe');
            const statusDiv = document.getElementById('status');
            const xmlBase64 = '{xml_base64}';
            let isLoaded = false;
            let editorReady = false;
            
            // Decode base64 to get XML
            function getXmlContent() {{
                try {{
                    return atob(xmlBase64);
                }} catch (e) {{
                    console.error('Error decoding XML:', e);
                    return '';
                }}
            }}
            
            function showStatus(message, duration = 2000) {{
                statusDiv.textContent = message;
                statusDiv.classList.add('show');
                setTimeout(() => {{
                    statusDiv.classList.remove('show');
                }}, duration);
            }}
            
            function loadDiagram() {{
                if (!editorReady) {{
                    showStatus('⏳ Editor not ready yet...', 1500);
                    return;
                }}
                
                try {{
                    const xmlContent = getXmlContent();
                    const message = {{
                        action: 'load',
                        xml: xmlContent,
                        autosave: 0
                    }};
                    
                    iframe.contentWindow.postMessage(JSON.stringify(message), '*');
                    showStatus('✅ Diagram loaded!', 2000);
                    isLoaded = true;
                }} catch (error) {{
                    showStatus('❌ Error loading diagram: ' + error.message, 3000);
                    console.error('Load error:', error);
                }}
            }}
            
            function exportDiagram() {{
                if (!editorReady) {{
                    showStatus('⏳ Editor not ready yet...', 1500);
                    return;
                }}
                
                try {{
                    const message = {{
                        action: 'export',
                        format: 'xml',
                        xml: '',
                        spin: 'Updating...'
                    }};
                    
                    iframe.contentWindow.postMessage(JSON.stringify(message), '*');
                    showStatus('📤 Requesting export...', 1500);
                }} catch (error) {{
                    showStatus('❌ Export error: ' + error.message, 3000);
                    console.error('Export error:', error);
                }}
            }}
            
            function exportPNG() {{
                if (!editorReady) {{
                    showStatus('⏳ Editor not ready yet...', 1500);
                    return;
                }}
                
                try {{
                    const message = {{
                        action: 'export',
                        format: 'png',
                        xml: '',
                        spin: 'Exporting...'
                    }};
                    
                    iframe.contentWindow.postMessage(JSON.stringify(message), '*');
                    showStatus('📤 Exporting PNG...', 2000);
                }} catch (error) {{
                    showStatus('❌ PNG export error: ' + error.message, 3000);
                    console.error('PNG export error:', error);
                }}
            }}
            
            // Listen for messages from draw.io
            window.addEventListener('message', function(event) {{
                // Security: Only accept messages from diagrams.net domain
                if (!event.origin.includes('diagrams.net') && !event.origin.includes('draw.io')) {{
                    return;
                }}
                
                    try {{
                    if (typeof event.data === 'string' && event.data.length > 0) {{
                        const msg = JSON.parse(event.data);
                        
                        if (msg.event === 'init') {{
                            editorReady = true;
                            showStatus('✅ Editor ready!', 2000);
                            // Auto-load after a short delay
                            setTimeout(loadDiagram, 500);
                        }} else if (msg.event === 'export') {{
                            if (msg.format === 'xml') {{
                                // Handle exported XML
                                const blob = new Blob([msg.data], {{ type: 'application/xml' }});
                                const url = URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url;
                                a.download = 'diagram_' + new Date().getTime() + '.drawio';
                                document.body.appendChild(a);
                                a.click();
                                document.body.removeChild(a);
                                URL.revokeObjectURL(url);
                                showStatus('✅ XML exported!', 2000);
                            }} else if (msg.format === 'png') {{
                                // Handle exported PNG
                                const blob = new Blob([msg.data], {{ type: 'image/png' }});
                                const url = URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url;
                                a.download = 'diagram_' + new Date().getTime() + '.png';
                                document.body.appendChild(a);
                                a.click();
                                document.body.removeChild(a);
                                URL.revokeObjectURL(url);
                                showStatus('✅ PNG exported!', 2000);
                            }}
                        }} else if (msg.event === 'save') {{
                            showStatus('💾 Changes saved!', 2000);
                        }}
                    }}
                }} catch (e) {{
                    // Ignore parse errors for non-JSON messages
                    if (e.name !== 'SyntaxError') {{
                        console.error('Message handler error:', e);
                    }}
                }}
            }});
            
            // Fallback: Try to load after iframe loads
            iframe.addEventListener('load', function() {{
                setTimeout(function() {{
                    if (!isLoaded && !editorReady) {{
                        editorReady = true;
                        setTimeout(loadDiagram, 1000);
                    }}
                }}, 2000);
            }});
            
            // Initial status
            showStatus('⏳ Loading editor...', 2000);
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=800)

def export_to_json(nodes, edges, clusters):
    """Export diagram data to JSON format."""
    return json.dumps({
        "metadata": {
            "version": "2.0",
            "created": datetime.now().isoformat(),
            "node_count": len(nodes),
            "edge_count": len(edges),
            "cluster_count": len(clusters)
        },
        "nodes": {nid: label for nid, label in nodes.items()},
        "edges": [{"source": e[0], "target": e[1], "label": e[2] if len(e) > 2 else ""} for e in edges],
        "clusters": [{"id": c["id"], "title": c["title"], "nodes": list(c["nodes"])} for c in clusters]
    }, indent=2)

def export_to_pdf(svg_code):
    """Export SVG to PDF using weasyprint or similar."""
    try:
        # For now, return SVG wrapped in HTML that can be printed to PDF
        # In production, you'd use weasyprint or reportlab
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @page {{ size: A4 landscape; margin: 20mm; }}
                body {{ margin: 0; padding: 20px; }}
                svg {{ max-width: 100%; height: auto; }}
            </style>
        </head>
        <body>
            {svg_code}
        </body>
        </html>
        """
        return html_content.encode('utf-8')
    except Exception as e:
        raise Exception(f"PDF export failed: {e}")

def export_to_svg_file(svg_code):
    """Export clean SVG file."""
    # Remove any wrapper divs and return pure SVG
    svg_match = re.search(r'<svg[^>]*>.*?</svg>', svg_code, re.DOTALL)
    if svg_match:
        return svg_match.group(0)
    return svg_code

def load_from_json(json_str):
    """Load diagram data from JSON format."""
    try:
        data = json.loads(json_str)
        nodes = data.get("nodes", {})
        edges = [(e["source"], e["target"], e.get("label", "")) for e in data.get("edges", [])]
        clusters = []
        for c in data.get("clusters", []):
            clusters.append({"id": c["id"], "title": c["title"], "nodes": set(c["nodes"])})
        return nodes, edges, clusters
    except Exception as e:
        raise ValueError(f"Invalid JSON format: {e}")

def validate_diagram_text(text):
    """Validate diagram text and return errors/warnings."""
    errors = []
    warnings = []
    
    if not text or not text.strip():
        errors.append("Diagram text is empty. Please enter some content.")
        return errors, warnings
    
    lines = text.split('\n')
    has_cluster = False
    has_nodes = False
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        # Check for clusters
        if line.startswith('#'):
            has_cluster = True
            if len(line) > 100:
                warnings.append(f"Line {i}: Cluster title is very long (>{len(line)} chars)")
        
        # Check for nodes
        if any(arrow in line for arrow in ['→', '->', '=>']):
            has_nodes = True
            # Check for unbalanced brackets
            if line.count('[') != line.count(']'):
                errors.append(f"Line {i}: Unbalanced brackets in edge labels")
        
        # Check for invalid characters
        if any(char in line for char in ['<', '>']):
            warnings.append(f"Line {i}: Contains potentially problematic characters (< or >)")
    
    if not has_nodes and not has_cluster:
        warnings.append("No nodes or clusters detected. Make sure to use arrows (→, ->, =>) or cluster markers (#)")
    
    return errors, warnings

def make_svg_interactive(svg_code, clusters, search_term=""):
    """Add JavaScript interactivity: collapsible clusters, zoom/pan, and search."""
    cluster_data = {c["id"]: c["title"] for c in clusters} if clusters else {}
    
    js_code = f"""
    <script>
    (function() {{
        const clusterData = {json.dumps(cluster_data)};
        const searchTerm = {json.dumps(search_term.lower())};
        const container = document.currentScript.previousElementSibling;
        const svg = container.querySelector('svg') || container;
        
        if (!svg) return;
        
        // Zoom and Pan functionality
        let scale = 1;
        let panX = 0;
        let panY = 0;
        let isPanning = false;
        let startX, startY;
        
        // Add zoom controls with better styling
        const zoomControls = document.createElement('div');
        zoomControls.style.cssText = 'position: absolute; top: 15px; right: 15px; z-index: 1000; background: rgba(255, 255, 255, 0.95); padding: 10px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); display: flex; gap: 6px; align-items: center; backdrop-filter: blur(10px); border: 1px solid rgba(0,0,0,0.1);';
        zoomControls.innerHTML = `
            <button id="zoom-in" title="Zoom In (Ctrl + Plus)" style="padding: 8px 12px; border: 1px solid #ddd; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; cursor: pointer; border-radius: 6px; font-size: 16px; font-weight: bold; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">➕</button>
            <button id="zoom-out" title="Zoom Out (Ctrl + Minus)" style="padding: 8px 12px; border: 1px solid #ddd; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; cursor: pointer; border-radius: 6px; font-size: 16px; font-weight: bold; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">➖</button>
            <button id="zoom-fit" title="Fit to Screen" style="padding: 8px 12px; border: 1px solid #ddd; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; cursor: pointer; border-radius: 6px; font-size: 16px; font-weight: bold; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">🔍</button>
            <button id="zoom-reset" title="Reset Zoom" style="padding: 8px 12px; border: 1px solid #ddd; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; cursor: pointer; border-radius: 6px; font-size: 16px; font-weight: bold; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">↺</button>
            <span id="zoom-level" style="padding: 8px 12px; font-size: 14px; font-weight: 600; color: #333; min-width: 60px; text-align: center; background: #f8f9fa; border-radius: 6px; border: 1px solid #e0e0e0;">100%</span>
        `;
        container.style.position = 'relative';
        container.appendChild(zoomControls);
        
        // Add hover effects for buttons
        ['zoom-in', 'zoom-out', 'zoom-fit', 'zoom-reset'].forEach(id => {{
            const btn = document.getElementById(id);
            btn.addEventListener('mouseenter', function() {{
                this.style.transform = 'scale(1.1)';
                this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
            }});
            btn.addEventListener('mouseleave', function() {{
                this.style.transform = 'scale(1)';
                this.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
            }});
        }});
        
        const svgWrapper = document.createElement('div');
        svgWrapper.style.cssText = 'overflow: auto; width: 100%; height: calc(100% - 50px); position: relative; box-sizing: border-box;';
        svgWrapper.appendChild(svg);
        container.insertBefore(svgWrapper, zoomControls);
        
        // Ensure SVG doesn't overflow its container
        svg.style.maxWidth = '100%';
        svg.style.height = 'auto';
        svg.style.display = 'block';
        
        function applyTransform() {{
            svg.style.transform = `translate(${{panX}}px, ${{panY}}px) scale(${{scale}})`;
            svg.style.transformOrigin = '0 0';
            document.getElementById('zoom-level').textContent = Math.round(scale * 100) + '%';
        }}
        
        document.getElementById('zoom-in').addEventListener('click', () => {{
            scale = Math.min(scale * 1.2, 5);
            applyTransform();
        }});
        
        document.getElementById('zoom-out').addEventListener('click', () => {{
            scale = Math.max(scale / 1.2, 0.1);
            applyTransform();
        }});
        
        document.getElementById('zoom-fit').addEventListener('click', () => {{
            const bbox = svg.getBBox();
            const containerWidth = container.clientWidth - 40;
            const containerHeight = container.clientHeight - 40;
            scale = Math.min(containerWidth / bbox.width, containerHeight / bbox.height, 1);
            panX = (containerWidth - bbox.width * scale) / 2 - bbox.x * scale;
            panY = (containerHeight - bbox.height * scale) / 2 - bbox.y * scale;
            applyTransform();
        }});
        
        document.getElementById('zoom-reset').addEventListener('click', () => {{
            scale = 1;
            panX = 0;
            panY = 0;
            applyTransform();
        }});
        
        // Pan with mouse drag
        svgWrapper.addEventListener('mousedown', (e) => {{
            if (e.button === 1 || (e.button === 0 && e.ctrlKey)) {{
                isPanning = true;
                startX = e.clientX - panX;
                startY = e.clientY - panY;
                svgWrapper.style.cursor = 'grabbing';
                e.preventDefault();
            }}
        }});
        
        svgWrapper.addEventListener('mousemove', (e) => {{
            if (isPanning) {{
                panX = e.clientX - startX;
                panY = e.clientY - startY;
                applyTransform();
            }}
        }});
        
        svgWrapper.addEventListener('mouseup', () => {{
            isPanning = false;
            svgWrapper.style.cursor = 'default';
        }});
        
        svgWrapper.addEventListener('mouseleave', () => {{
            isPanning = false;
            svgWrapper.style.cursor = 'default';
        }});
        
        // Mouse wheel zoom
        svgWrapper.addEventListener('wheel', (e) => {{
            if (e.ctrlKey || e.metaKey) {{
                e.preventDefault();
                const delta = e.deltaY > 0 ? 0.9 : 1.1;
                const rect = svgWrapper.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const oldScale = scale;
                scale = Math.max(0.1, Math.min(5, scale * delta));
                
                // Zoom towards mouse position
                const scaleChange = scale / oldScale;
                panX = x - (x - panX) * scaleChange;
                panY = y - (y - panY) * scaleChange;
                
                applyTransform();
            }}
        }}, {{ passive: false }});
        
        // Keyboard shortcuts for zoom
        document.addEventListener('keydown', (e) => {{
            if ((e.ctrlKey || e.metaKey) && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {{
                if (e.key === '+' || e.key === '=') {{
                    e.preventDefault();
                    document.getElementById('zoom-in').click();
                }} else if (e.key === '-' || e.key === '_') {{
                    e.preventDefault();
                    document.getElementById('zoom-out').click();
                }} else if (e.key === '0') {{
                    e.preventDefault();
                    document.getElementById('zoom-reset').click();
                }}
            }}
        }});
        
        // Search functionality - improved
        function performSearch() {{
            if (!searchTerm) {{
                // Reset all text styles when search is cleared
                const allTexts = svg.querySelectorAll('text');
                allTexts.forEach(text => {{
                    text.style.fill = '';
                    text.style.fontWeight = '';
                    text.style.fontSize = '';
                }});
                return;
            }}
            
            const allTexts = svg.querySelectorAll('text');
            let found = false;
            let firstFound = null;
            
            allTexts.forEach(text => {{
                const textContent = (text.textContent || '').toLowerCase();
                if (textContent.includes(searchTerm)) {{
                    found = true;
                    if (!firstFound) firstFound = text;
                    
                    // Highlight found text
                    text.style.fill = '#ff0000';
                    text.style.fontWeight = 'bold';
                    const currentSize = parseFloat(window.getComputedStyle(text).fontSize) || 12;
                    text.style.fontSize = (currentSize * 1.2) + 'px';
                    
                    // Also highlight parent node if it's a tspan
                    let parent = text.parentElement;
                    if (parent && parent.tagName === 'tspan') {{
                        parent = parent.parentElement;
                    }}
                    if (parent && (parent.tagName === 'g' || parent.tagName === 'text')) {{
                        parent.style.filter = 'drop-shadow(0 0 3px #ff0000)';
                    }}
                }} else {{
                    // Reset non-matching text
                    text.style.fill = '';
                    text.style.fontWeight = '';
                    text.style.fontSize = '';
                }}
            }});
            
            // Scroll to first found element
            if (firstFound) {{
                try {{
                    const bbox = firstFound.getBBox();
                    const containerWidth = svgWrapper.clientWidth;
                    const containerHeight = svgWrapper.clientHeight;
                    panX = containerWidth / 2 - (bbox.x + bbox.width / 2) * scale;
                    panY = containerHeight / 2 - (bbox.y + bbox.height / 2) * scale;
                    applyTransform();
                }} catch (e) {{
                    console.log('Could not scroll to element:', e);
                }}
            }}
        }}
        
        // Perform search on load and when search term changes
        if (searchTerm) {{
            performSearch();
        }}
        
        // Watch for search term changes (if search input is in the same container)
        const searchInput = document.querySelector('input[placeholder*="search" i], input[placeholder*="Search" i]');
        if (searchInput) {{
            searchInput.addEventListener('input', function() {{
                const newSearchTerm = this.value.toLowerCase();
                if (newSearchTerm !== searchTerm) {{
                    searchTerm = newSearchTerm;
                    performSearch();
                }}
            }});
        }}
        
        // Collapsible clusters
        Object.keys(clusterData).forEach(clusterId => {{
            const clusterGroups = svg.querySelectorAll('g[id*="' + clusterId + '"]');
            clusterGroups.forEach(clusterGroup => {{
                const titleTexts = clusterGroup.querySelectorAll('text');
                titleTexts.forEach(title => {{
                    const textContent = title.textContent || '';
                    if (textContent.includes(clusterData[clusterId])) {{
                        title.style.cursor = 'pointer';
                        title.style.fontWeight = 'bold';
                        title.style.fill = '#0066cc';
                        title.setAttribute('data-cluster-id', clusterId);
                        title.setAttribute('data-expanded', 'true');
                        
                        title.addEventListener('mouseenter', function() {{
                            this.style.fill = '#004499';
                            this.style.textDecoration = 'underline';
                        }});
                        
                        title.addEventListener('mouseleave', function() {{
                            if (this.getAttribute('data-expanded') === 'true') {{
                                this.style.fill = '#0066cc';
                            }}
                            this.style.textDecoration = 'none';
                        }});
                        
                        title.addEventListener('click', function(e) {{
                            e.stopPropagation();
                            const isExpanded = this.getAttribute('data-expanded') === 'true';
                            const cId = this.getAttribute('data-cluster-id');
                            
                            const allGroups = svg.querySelectorAll('g');
                            allGroups.forEach(group => {{
                                if (group.id && group.id.includes(cId)) {{
                                    const isTitle = group.querySelector('text') === this;
                                    if (!isTitle) {{
                                        group.style.display = isExpanded ? 'none' : 'block';
                                        group.style.opacity = isExpanded ? '0' : '1';
                                        group.style.transition = 'opacity 0.3s ease';
                                    }}
                                }}
                            }});
                            
                            this.setAttribute('data-expanded', isExpanded ? 'false' : 'true');
                            let newText = textContent.replace(' [Collapsed]', '').replace(' [Expanded]', '');
                            newText += isExpanded ? ' [Collapsed]' : ' [Expanded]';
                            this.textContent = newText;
                            this.style.fill = isExpanded ? '#999999' : '#0066cc';
                        }});
                    }}
                }});
            }});
        }});
        
        // Initial fit
        setTimeout(() => {{
            document.getElementById('zoom-fit').click();
        }}, 100);
    }})();
    </script>
    """
    
    return f'<div id="svg-container" style="position: relative; width: 100%; height: 100%; max-width: 100%; box-sizing: border-box; overflow: hidden;">{svg_code}</div>{js_code}'

@st.cache_data(ttl=300)
def cached_render_svg(dot_code_hash, dot_code):
    """Cache SVG rendering to improve performance."""
    try:
        resp = requests.post(
            "https://quickchart.io/graphviz", 
            json={"graph": dot_code, "format": "svg"}, 
            timeout=15
        )
        if resp.status_code == 200:
            svg_code = resp.text
            svg_code = re.sub(r'width=".*?"', 'width="100%"', svg_code, count=1)
            svg_code = re.sub(r'height=".*?"', '', svg_code, count=1)
            return svg_code, None
        return None, f"Service returned status {resp.status_code}"
    except Exception as e:
        return None, str(e)

PRESETS = {
    "Full Authentication": """## Authentication Flow
User Arrives → Login Dialog → Enter Credentials
↓
POST /auth/login → Validate Credentials → Check Environment Access
↓
Success: Generate JWT Token → Store Session
↓
Redirect to Dashboard""",
    "Design Mode": """## Design Mode
Dashboard → Design Mode → Upload File (Excel/FBDI/Schema)
↓
POST /api/design/upload → Extract Metadata → Parse Structure
↓
Display File Tree → Select Source & Target → Open Mapping Drawer
↓
Auto-Mapping OR Manual Mapping → Configure Validation Rules
↓
POST /api/design/configs → Save Configuration → Store in Database""",
    "Data Migration Flow": """## Data Migration
User → Dashboard → Select Source Database
↓
Connect to Source DB → Extract Schema → Validate Connection
↓
Select Target Database → Map Tables [Auto-Map] → Review Mappings
↓
Start Migration → Monitor Progress → Validate Data
↓
Success → Generate Report → Store Logs in Database""",
    "API Integration": """## API Integration Flow
Client Application → API Gateway → Authentication Service
↓
Validate Token → Route Request → Process Business Logic
↓
Query Database → Transform Data → Return Response
↓
Error Handling → Log Events → Send Notification [Email]""",
    "Microservices Architecture": """## Microservices
User Interface → API Gateway → Service Discovery
↓
Auth Service → User Service → Order Service
↓
Payment Service → Notification Service → Database Cluster
↓
Message Queue → Event Bus → Logging Service""",
    "Simple Flow": """## Simple Process
Start → Step 1 → Step 2 → Step 3 → End""",
    "E-Commerce Flow": """## E-Commerce System
Customer → Browse Products → Add to Cart
↓
Checkout → Payment Gateway → Process Payment
↓
Order Confirmation → Inventory Update → Shipping Service
↓
Email Notification → Track Order → Delivery Complete""",
    "CI/CD Pipeline": """## CI/CD Pipeline
Developer → Push Code → Git Repository
↓
Trigger Build → Run Tests → Code Quality Check
↓
Build Docker Image → Push to Registry → Deploy to Staging
↓
Integration Tests → Deploy to Production → Monitor Health""",
    "Microservices Mind Map": """## Microservices Architecture
API Gateway
↓
Auth Service → User Service → Order Service
↓
Payment Service → Notification Service → Analytics Service
↓
Database Cluster → Cache Layer → Message Queue""",
    "Design Mode - Create Configuration": """## Create New Configuration
User Opens Design Mode → Sees List of Existing Configurations
↓
User Clicks "New Configuration" → Enters Configuration Name → Clicks "Create"
↓
User Uploads Source File → Selects File from Computer → File Uploads → System Shows File Preview
↓
User Reviews File Columns → Sees All Columns from File → User Maps Each Column
↓
User Maps Column → Selects Source Column → Selects Target Field → Clicks "Map"
↓
User Maps All Columns → Reviews Mappings → Clicks "Save Configuration"
↓
Configuration Saved → System Shows Success Message → Configuration Appears in List""",
    "Design Mode - Edit Configuration": """## Edit Existing Configuration
User Opens Design Mode → Sees List of Configurations → User Clicks on Configuration
↓
System Shows Configuration Details → User Sees All Mapped Fields → User Can Modify Mappings
↓
User Changes Mapping → Selects Different Target Field → Clicks "Update"
↓
User Makes All Changes → Clicks "Save" → Configuration Updated → System Shows Success Message""",
    "Design Mode - Use Template": """## Use Template
User Opens Design Mode → Clicks "Templates" → Sees List of Templates
↓
User Selects Template → System Loads Template → Pre-fills Configuration Form
↓
User Reviews Template Settings → User Can Modify Settings → User Clicks "Use Template"
↓
Template Applied → User Can Edit as Needed → User Saves as New Configuration""",
    "Design Mode - Delete Configuration": """## Delete Configuration
User Opens Design Mode → Sees Configuration List → User Selects Configuration
↓
User Clicks "Delete" → System Asks for Confirmation → User Confirms Deletion
↓
Configuration Deleted → Removed from List → System Shows Success Message""",
    "Design Mode - Complete Flow": """## Design Mode Complete User Flow
## Create New Configuration
User Opens Design Mode → Sees List of Existing Configurations
↓
User Clicks "New Configuration" → Enters Configuration Name → Clicks "Create"
↓
User Uploads Source File → File Uploads → System Shows File Preview
↓
User Reviews File Columns → User Maps Each Column → Clicks "Save Configuration"
↓
Configuration Saved → System Shows Success Message
↓
## Edit Existing Configuration
User Clicks on Configuration → System Shows Configuration Details
↓
User Modifies Mappings → Clicks "Save" → Configuration Updated
↓
## Use Template
User Clicks "Templates" → Selects Template → System Pre-fills Form
↓
User Reviews Settings → Clicks "Use Template" → Saves as New Configuration
↓
## Delete Configuration
User Selects Configuration → Clicks "Delete" → Confirms Deletion
↓
Configuration Deleted → Removed from List"""
}

# --- Sidebar ---
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
    <h1 style="color: white; margin: 0; font-size: 1.8rem; text-align: center;">🏗️ Auto-Architect</h1>
    <p style="color: rgba(255, 255, 255, 0.9); margin: 0.5rem 0 0 0; text-align: center; font-size: 0.9rem;">Convert text flows into innovative visual systems</p>
</div>
""", unsafe_allow_html=True)

# Save/Load Section
st.sidebar.markdown("### 💾 Save & Load")
st.sidebar.markdown("---")
if "saved_diagrams" not in st.session_state:
    st.session_state.saved_diagrams = {}

save_name = st.sidebar.text_input(
    "Save as:", 
    placeholder="my_diagram", 
    key="save_name_input",
    help="Enter a name for your diagram (optional)"
)
if st.sidebar.button("💾 Save Diagram", use_container_width=True, key="save_btn"):
    # Get current text from the text area
    current_text = st.session_state.get("main_input", st.session_state.get("text_input", ""))
    if current_text and current_text.strip():
        diagram_name = save_name.strip() if save_name and save_name.strip() else f"diagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state.saved_diagrams[diagram_name] = {
            "text": current_text,
            "timestamp": datetime.now().isoformat()
        }
        st.session_state.text_input = current_text  # Sync with session state
        st.sidebar.success(f"✅ Saved as '{diagram_name}'!")
        st.rerun()
    else:
        st.sidebar.warning("⚠️ No diagram to save. Please enter some text first.")

if st.session_state.saved_diagrams:
    load_diagram = st.sidebar.selectbox("Load saved:", [""] + list(st.session_state.saved_diagrams.keys()), key="load_select")
    
    col_load, col_del = st.sidebar.columns(2)
    with col_load:
        if load_diagram and st.button("📂 Load", use_container_width=True, key="load_btn"):
            if load_diagram in st.session_state.saved_diagrams:
                loaded_text = st.session_state.saved_diagrams[load_diagram]["text"]
                st.session_state.text_input = loaded_text
                st.session_state.main_input = loaded_text  # Update the text area
                st.session_state.last_preset = None  # Reset preset so it doesn't override
                st.sidebar.success(f"✅ Loaded '{load_diagram}'!")
                st.rerun()
    
    with col_del:
        if load_diagram and st.button("🗑️ Delete", use_container_width=True, key="delete_btn"):
            if load_diagram in st.session_state.saved_diagrams:
                del st.session_state.saved_diagrams[load_diagram]
                st.sidebar.success(f"✅ Deleted '{load_diagram}'!")
                st.rerun()
    
    # Show saved diagrams list
    with st.sidebar.expander("📋 View All Saved Diagrams"):
        for name, data in st.session_state.saved_diagrams.items():
            st.caption(f"**{name}** - {data.get('timestamp', 'Unknown date')[:10]}")
else:
    st.sidebar.info("💡 No saved diagrams yet. Create one to get started!")

st.sidebar.markdown("---")

selected_preset = st.sidebar.selectbox(
    "📋 Load Preset", 
    list(PRESETS.keys()),
    help="Choose a preset template to start with"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Visualization Mode")

visualization_mode = st.sidebar.selectbox(
    "Diagram Type",
    ["flow", "sequence", "mindmap", "network"],
    format_func=lambda x: {
        "flow": "📊 Flow Diagram",
        "sequence": "🔄 Sequence Diagram", 
        "mindmap": "🧠 Mind Map",
        "network": "🌐 Network Diagram"
    }[x],
    help="Choose the visualization style - Flow for processes, Sequence for interactions, Mind Map for ideas, Network for connections."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Styling & Layout")

selected_theme = st.sidebar.selectbox(
    "Visual Theme", 
    list(THEMES.keys()), 
    index=0,
    help="Choose a color theme for your diagram"
)
layout_engine = st.sidebar.selectbox(
    "Layout Structure", 
    ["Hierarchy (Waterfall)", "Organic (Force)", "Circular (Ring)", "Radial (Star)", "Freeform"],
    help="Change the fundamental shape of the diagram"
)
splines = st.sidebar.selectbox(
    "Line Style", 
    ["ortho", "curved", "polyline"],
    help="Choose how connections are drawn"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Settings")

# Auto-refresh toggle
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh", value=st.session_state.auto_refresh, help="Automatically update diagram as you type")
st.session_state.auto_refresh = auto_refresh

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Use `[label]` on arrows to add edge labels. Icons are auto-added based on keywords. Click cluster titles to collapse/expand!")

# --- Header with Branding ---
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); padding: 1.5rem 2rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3); display: flex; justify-content: space-between; align-items: center;">
    <div>
        <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: bold; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">🌙 Dark VizMate</h1>
        <p style="color: rgba(255, 255, 255, 0.9); margin: 0.5rem 0 0 0; font-size: 1rem;">Transform text into stunning visual architectures</p>
    </div>
    <div style="text-align: right;">
        <p style="color: rgba(255, 255, 255, 0.8); margin: 0; font-size: 0.9rem;">© 2024 Kunal/Dark</p>
        <p style="color: rgba(255, 255, 255, 0.7); margin: 0.3rem 0 0 0; font-size: 0.85rem;">All Rights Reserved</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Main UI ---
# Use more balanced column layout
col1, col2 = st.columns([1.2, 1.8], gap="large")

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
        <h3 style="color: white; margin: 0; text-align: center;">📝 Input</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload option for .md files
    st.markdown("#### 📄 Upload Markdown File")
    uploaded_file = st.file_uploader(
        "Choose a .md file",
        type=['md', 'markdown'],
        help="Upload a Markdown file containing your diagram flow. The content will be automatically loaded into the editor.",
        key="md_file_uploader"
    )
    
    if uploaded_file is not None:
        try:
            # Read the file content
            file_content = uploaded_file.read().decode('utf-8')
            
            # Update session state with file content
            st.session_state.text_input = file_content
            st.session_state.main_input = file_content
            st.session_state.last_preset = None  # Reset preset so it doesn't override
            
            st.success(f"✅ Successfully loaded '{uploaded_file.name}'!")
            st.info(f"📄 File size: {len(file_content)} characters")
            
            # Show a preview of the content
            with st.expander("📋 Preview File Content", expanded=False):
                st.code(file_content, language="markdown")
            
            st.rerun()
        except UnicodeDecodeError as e:
            st.error("❌ **File Encoding Error**")
            st.error("Could not decode the file. Please ensure it's a valid UTF-8 encoded file.")
            st.warning("💡 **Solution:** Save your file as UTF-8 encoding and try again.")
            with st.expander("🔍 Technical Details", expanded=False):
                st.exception(e)
        except Exception as e:
            error_type = type(e).__name__
            st.error(f"❌ **Error Reading File**")
            st.error(f"**Error Type:** {error_type}")
            st.error(f"**Message:** {str(e)}")
            st.warning("💡 **Troubleshooting:**\n"
                      "- Ensure the file is a valid Markdown (.md) file\n"
                      "- Check if the file is not corrupted\n"
                      "- Try opening the file in a text editor first")
            with st.expander("🔍 Technical Details", expanded=False):
                st.exception(e)
    
    st.markdown("---")
    
    # Quick Help Section with Downloads
    with st.expander("📚 Help & Resources", expanded=False):
        col_help1, col_help2 = st.columns(2, gap="medium")
        
        with col_help1:
            # Read sample format file
            try:
                with open("sample_diagram_format.txt", "r", encoding="utf-8") as f:
                    sample_format_content = f.read()
                st.download_button(
                    "📄 Sample Format File",
                    sample_format_content,
                    "sample_diagram_format.txt",
                    "text/plain",
                    use_container_width=True,
                    help="Download a template with examples of the correct format"
                )
            except FileNotFoundError:
                st.warning("⚠️ Sample format file not found")
        
        with col_help2:
            # Read conversion manual
            try:
                with open("CONVERSION_MANUAL.md", "r", encoding="utf-8") as f:
                    manual_content = f.read()
                st.download_button(
                    "📘 Conversion Manual",
                    manual_content,
                    "CONVERSION_MANUAL.md",
                    "text/markdown",
                    use_container_width=True,
                    help="Complete guide for converting text to diagram format"
                )
            except FileNotFoundError:
                st.warning("⚠️ Conversion manual not found")
        
        st.info("""
        **💡 Quick Conversion Workflow:**
        1. Download both files above
        2. Open VS Code → Open your source file
        3. Open the Conversion Manual in split view
        4. Follow the manual to convert your text
        5. Copy and paste here to generate diagram!
        """)
    
    st.markdown("---")
    
    if "text_input" not in st.session_state: st.session_state.text_input = PRESETS[selected_preset]
    if "last_preset" not in st.session_state or st.session_state.last_preset != selected_preset:
        st.session_state.text_input = PRESETS[selected_preset]
        st.session_state.last_preset = selected_preset
    
    # Validation - Sync text area with session state
    if "text_input" not in st.session_state:
        st.session_state.text_input = PRESETS[selected_preset]
    
    # Update session state when text area changes
    user_text = st.text_area(
        "Paste flows or edit uploaded content:", 
        value=st.session_state.text_input, 
        height=550, 
        key="main_input",
        help="Enter your diagram flow using arrows (→) and clusters (#), or edit content from uploaded file"
    )
    
    # Sync user_text back to session_state for save/load functionality
    if user_text != st.session_state.get("text_input", ""):
        st.session_state.text_input = user_text
    
    # Auto-refresh logic (moved here after user_text is defined)
    if auto_refresh and user_text:
        # Use a small delay to avoid too frequent updates
        import time
        if "last_update" not in st.session_state:
            st.session_state.last_update = time.time()
        elif time.time() - st.session_state.last_update > 1.5:  # Update every 1.5 seconds
            st.session_state.last_update = time.time()
            # The rerun will happen naturally when text changes
    
    # Validate input with better layout
    if user_text:
        errors, warnings = validate_diagram_text(user_text)
        if errors:
            st.markdown("---")
            for error in errors:
                st.error(f"❌ {error}")
        if warnings:
            st.markdown("---")
            for warning in warnings:
                st.warning(f"⚠️ {warning}")
    
    # Auto-refresh indicator
    if auto_refresh:
        st.markdown("---")
        st.caption("🔄 **Auto-refresh enabled** - diagram updates automatically as you type")

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1rem; border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);">
        <h3 style="color: white; margin: 0; text-align: center;">✨ Visual System</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if user_text:
        try:
            # Validate before parsing
            errors, warnings = validate_diagram_text(user_text)
            if errors:
                st.error("❌ **Validation Errors Found**")
                st.error("Please fix the following errors before generating the diagram:")
                for i, error in enumerate(errors, 1):
                    st.error(f"{i}. {error}")
                st.info("💡 **Tip:** Check the syntax guide below for help with proper formatting.")
            else:
                nodes, edges, clusters = parse_diagram_data(user_text)
                
                # Generate DOT with visualization mode
                collapsed_clusters = set()  # Keep for function signature but don't show UI controls
                dot_code = generate_dot_code(nodes, edges, clusters, selected_theme, layout_engine, splines, visualization_mode, collapsed_clusters)
                drawio_xml = generate_drawio_xml(nodes, edges, clusters)
                
                # Search functionality with better layout
                search_col1, search_col2 = st.columns([3, 1])
                with search_col1:
                    search_term = st.text_input(
                        "🔍 Search nodes:", 
                        placeholder="Type to search nodes...", 
                        key="search_input",
                        help="Search for specific nodes in the diagram"
                    )
                with search_col2:
                    st.write("")  # Spacer
                    st.write("")  # Spacer
                    if search_term:
                        st.caption(f"🔎 {len([n for n in nodes.values() if search_term.lower() in n.lower()])} found")
                
                # Display stats with colorful cards
                st.markdown("<br>", unsafe_allow_html=True)
                col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4, gap="small")
                
                with col_stats1:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                        <div style="color: white; font-size: 2rem; font-weight: bold;">{len(nodes)}</div>
                        <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem;">Nodes</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_stats2:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 8px rgba(240, 147, 251, 0.3);">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔗</div>
                        <div style="color: white; font-size: 2rem; font-weight: bold;">{len(edges)}</div>
                        <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem;">Edges</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_stats3:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 8px rgba(79, 172, 254, 0.3);">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📦</div>
                        <div style="color: white; font-size: 2rem; font-weight: bold;">{len(clusters)}</div>
                        <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem;">Clusters</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_stats4:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 1rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 8px rgba(250, 112, 154, 0.3);">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎨</div>
                        <div style="color: white; font-size: 1.2rem; font-weight: bold;">{visualization_mode.title()}</div>
                        <div style="color: rgba(255, 255, 255, 0.9); font-size: 0.9rem;">Mode</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                tab1, tab2, tab3 = st.tabs(["📊 Smart View", "✏️ Visual Editor", "📥 Export"])
                with tab1:
                    png_data = None
                    svg_file_data = None

                    # 1. Fetch Responsive SVG for Screen with caching
                    try:
                        dot_hash = hashlib.md5(dot_code.encode()).hexdigest()
                        svg_code, error_msg = cached_render_svg(dot_hash, dot_code)
                        
                        if svg_code:
                            # Make interactive with zoom, pan, search, and collapsible clusters
                            svg_code = make_svg_interactive(svg_code, clusters, search_term)
                            
                            # Store clean SVG for export
                            svg_file_data = export_to_svg_file(svg_code)
                            
                            # Wrap in container with enhanced styling and proper overflow handling
                            container_style = f"""
                            width: 100%; 
                            max-width: 100%;
                            height: 650px;
                            max-height: 650px;
                            border: 2px solid {THEMES[selected_theme]['edge_color']}; 
                            border-radius: 12px; 
                            padding: 15px; 
                            background: {THEMES[selected_theme]['bgcolor']};
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.08);
                            overflow: auto;
                            position: relative;
                            box-sizing: border-box;
                            margin: 10px 0;
                            """
                            st.markdown(f"""<div style="{container_style}">{svg_code}</div>""", unsafe_allow_html=True)
                            
                            if search_term:
                                st.info(f"🔍 Searching for: '{search_term}' - Matching nodes are highlighted in red")
                            
                            # 2. Fetch High-Res PNG for Download Only
                            try:
                                dot_code_dl = dot_code.replace('graph {', 'graph { dpi=300; ')
                                resp_png = requests.post(
                                    "https://quickchart.io/graphviz", 
                                    json={"graph": dot_code_dl, "format": "png"}, 
                                    timeout=15
                                )
                                if resp_png.status_code == 200:
                                    png_data = resp_png.content
                            except Exception as png_err:
                                st.warning("⚠️ **PNG Generation Failed**")
                                st.warning(f"High-resolution PNG could not be generated: {str(png_err)}")
                                st.info("💡 The diagram is still available in SVG format. PNG export will be retried automatically.")
                                with st.expander("🔍 PNG Error Details", expanded=False):
                                    st.exception(png_err)
                        else:
                            st.error("❌ **Visualization Error**")
                            st.error(f"Could not generate diagram visualization.")
                            st.error(f"**Error:** {error_msg}")
                            st.warning("💡 **Troubleshooting:**\n"
                                      "- Check your diagram syntax\n"
                                      "- Try simplifying the diagram\n"
                                      "- The visualization service might be experiencing issues")
                    except Exception as e:
                        error_type = type(e).__name__
                        st.error("❌ **Visualizer Connection Issue**")
                        st.error(f"**Error Type:** {error_type}")
                        st.error(f"**Message:** {str(e)}")
                        st.warning("💡 **Troubleshooting:**\n"
                                  "- Check your internet connection\n"
                                  "- The visualization service might be temporarily unavailable\n"
                                  "- Try refreshing the page")
                        with st.expander("🔍 Technical Error Details", expanded=False):
                            st.exception(e)

                    st.markdown("---")
                    
                    # Quick download buttons with better layout
                    st.markdown("#### 📥 Quick Export")
                    c1, c2, c3, c4 = st.columns(4, gap="small")
                    with c1: 
                        st.download_button(
                            "📄 .drawio", 
                            drawio_xml, 
                            "arch.drawio", 
                            "application/xml", 
                            use_container_width=True,
                            help="Download as Draw.io format"
                        )
                    with c2: 
                        if png_data: 
                            st.download_button(
                                "🖼️ PNG", 
                                png_data, 
                                "arch.png", 
                                "image/png", 
                                use_container_width=True,
                                help="Download as PNG image"
                            )
                        else: 
                            st.info("⏳ PNG...", icon="⏳")
                    with c3:
                        if svg_file_data:
                            st.download_button(
                                "📐 SVG", 
                                svg_file_data.encode('utf-8'), 
                                "arch.svg", 
                                "image/svg+xml", 
                                use_container_width=True,
                                help="Download as SVG vector"
                            )
                        else:
                            st.info("⏳ SVG...", icon="⏳")
                    with c4:
                        with st.expander("🔍 DOT Code", expanded=False):
                            st.code(dot_code, language="dot")
                            
                with tab3:
                    st.markdown("### 📥 Export Options")
                    st.markdown("---")
                    
                    # Export format selection
                    export_format = st.radio(
                        "Select Export Format:",
                        ["PNG (Image)", "SVG (Vector)", "PDF (Document)", "JSON (Data)", "DOT (Graphviz)", "Draw.io XML"],
                        horizontal=True,
                        help="Choose the format you want to export your diagram in"
                    )
                    
                    st.markdown("---")
                    
                    if export_format == "PNG (Image)":
                        if png_data:
                            st.download_button(
                                "📥 Download PNG", 
                                png_data, 
                                "diagram.png", 
                                "image/png",
                                use_container_width=True
                            )
                        else:
                            st.info("⏳ Generating PNG... Please wait.")
                            
                    elif export_format == "SVG (Vector)":
                        if svg_file_data:
                            st.download_button(
                                "📥 Download SVG", 
                                svg_file_data.encode('utf-8'), 
                                "diagram.svg", 
                                "image/svg+xml",
                                use_container_width=True
                            )
                            st.caption("💡 SVG format is scalable and perfect for presentations and documents.")
                        else:
                            st.warning("SVG not available. Please generate a diagram first.")
                            
                    elif export_format == "PDF (Document)":
                        try:
                            # Get clean SVG for PDF
                            dot_hash = hashlib.md5(dot_code.encode()).hexdigest()
                            clean_svg, _ = cached_render_svg(dot_hash, dot_code)
                            if clean_svg:
                                pdf_data = export_to_pdf(clean_svg)
                                st.download_button(
                                    "📥 Download PDF", 
                                    pdf_data, 
                                    "diagram.pdf", 
                                    "application/pdf",
                                    use_container_width=True
                                )
                                st.caption("💡 PDF format is optimized for printing and sharing.")
                            else:
                                st.warning("Please generate a diagram first.")
                        except Exception as e:
                            error_type = type(e).__name__
                            st.error("❌ **PDF Export Error**")
                            st.error(f"**Error Type:** {error_type}")
                            st.error(f"**Message:** {str(e)}")
                            st.warning("💡 **Alternative Solutions:**\n"
                                      "- Use the browser's Print to PDF feature (Ctrl+P / Cmd+P)\n"
                                      "- Export as SVG and convert to PDF using an external tool\n"
                                      "- Export as PNG and convert to PDF")
                            with st.expander("🔍 PDF Error Details", expanded=False):
                                st.exception(e)
                            
                    elif export_format == "JSON (Data)":
                        json_data = export_to_json(nodes, edges, clusters)
                        st.download_button(
                            "📥 Download JSON", 
                            json_data, 
                            "diagram.json", 
                            "application/json",
                            use_container_width=True
                        )
                        st.caption("💡 JSON format allows you to import the diagram structure later.")
                        
                    elif export_format == "DOT (Graphviz)":
                        st.download_button(
                            "📥 Download DOT", 
                            dot_code.encode('utf-8'), 
                            "diagram.dot", 
                            "text/plain",
                            use_container_width=True
                        )
                        st.caption("💡 DOT format can be used with Graphviz command-line tools.")
                        
                    elif export_format == "Draw.io XML":
                        st.download_button(
                            "📥 Download Draw.io XML", 
                            drawio_xml, 
                            "diagram.drawio", 
                            "application/xml",
                            use_container_width=True
                        )
                        st.caption("💡 Draw.io format can be opened in draw.io or diagrams.net.")
                    
                    st.markdown("---")
                    st.markdown("### 📤 Import JSON")
                    uploaded_json = st.file_uploader(
                        "Upload JSON file", 
                        type=["json"],
                        help="Import a previously exported diagram JSON file"
                    )
                    if uploaded_json:
                        try:
                            json_content = uploaded_json.read().decode('utf-8')
                            loaded_nodes, loaded_edges, loaded_clusters = load_from_json(json_content)
                            
                            # Reconstruct text from loaded data
                            # This is a simplified reconstruction
                            reconstructed_text = ""
                            for c in loaded_clusters:
                                reconstructed_text += f"## {c['title']}\n"
                                cluster_nodes = [nid for nid in c['nodes'] if nid in loaded_nodes]
                                if cluster_nodes:
                                    reconstructed_text += " → ".join([loaded_nodes[nid] for nid in cluster_nodes]) + "\n"
                            
                            if st.button("📂 Load into Editor", use_container_width=True):
                                st.session_state.text_input = reconstructed_text
                                st.session_state.main_input = reconstructed_text
                                st.success("✅ Diagram loaded successfully!")
                                st.rerun()
                        except Exception as e:
                            error_type = type(e).__name__
                            st.error("❌ **JSON Import Error**")
                            st.error(f"**Error Type:** {error_type}")
                            st.error(f"**Message:** {str(e)}")
                            st.warning("💡 **Troubleshooting:**\n"
                                      "- Ensure the JSON file was exported from this application\n"
                                      "- Check if the JSON file is valid and not corrupted\n"
                                      "- Verify the file structure matches the expected format")
                            with st.expander("🔍 JSON Error Details", expanded=False):
                                st.exception(e)
                                st.code(f"Error Type: {error_type}\nError Message: {str(e)}", language="text")
                    
                    st.markdown("---")
                    st.markdown("### 📊 Diagram Statistics")
                    st.json({
                        "nodes": len(nodes),
                        "edges": len(edges),
                        "clusters": len(clusters),
                        "theme": selected_theme,
                        "layout": layout_engine,
                        "visualization_mode": visualization_mode,
                        "collapsed_clusters": len(collapsed_clusters)
                    })

            with tab2:
                st.markdown("### ✏️ Visual Editor")
                st.info("""
                **Full-featured draw.io editor embedded below!**
                - ✏️ **Edit**: Click and drag to move elements, double-click to edit text
                - ➕ **Add**: Use the toolbar on the left to add shapes, connectors, and more
                - 🎨 **Style**: Right-click elements to change colors, fonts, and styles
                - 💾 **Export**: Use the buttons in the top-right to export your edited diagram
                - 🔄 **Reload**: Click 'Reload' to restore the original diagram
                """)
                
                col_editor1, col_editor2 = st.columns([3, 1], gap="small")
                with col_editor1:
                    st.caption("💡 **Tip:** The editor is fully interactive - you can add, edit, and style any element!")
                with col_editor2:
                    if st.button("🔄 Refresh Editor", use_container_width=True):
                        st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
                render_drawio_editor(drawio_xml)
                
                st.markdown("---")
                st.markdown("#### 📥 Quick Export")
                st.caption("Use the export buttons in the editor above, or download the original diagram below:")
                st.download_button(
                    "📄 Download Original .drawio",
                    drawio_xml,
                    "diagram.drawio",
                    "application/xml",
                    use_container_width=True,
                    help="Download the original diagram in Draw.io format"
                )
        except Exception as e: 
            error_msg = str(e)
            error_type = type(e).__name__
            
            # Display main error message
            st.error(f"❌ **Error Processing Diagram**")
            st.error(f"**Error Type:** {error_type}")
            st.error(f"**Message:** {error_msg}")
            
            # Provide context-specific help based on error type
            if "parse" in error_msg.lower() or "syntax" in error_msg.lower() or "ParseError" in error_type:
                st.warning("⚠️ **Syntax Error Detected**")
                st.info("💡 **Syntax Help:**\n"
                       "- Use `#` for cluster titles\n"
                       "- Use `→`, `->`, or `=>` for connections\n"
                       "- Use `↓`, `v`, or `|` for vertical flow\n"
                       "- Check for balanced brackets `[` and `]`\n"
                       "- Ensure proper arrow syntax between nodes")
            elif "connection" in error_msg.lower() or "timeout" in error_msg.lower() or "network" in error_msg.lower():
                st.warning("⚠️ **Connection Issue**")
                st.info("💡 **Troubleshooting:**\n"
                       "- Check your internet connection\n"
                       "- The visualization service might be temporarily unavailable\n"
                       "- Try again in a few moments")
            elif "key" in error_msg.lower() or "KeyError" in error_type:
                st.warning("⚠️ **Configuration Error**")
                st.info("💡 **Solution:**\n"
                       "- Try selecting a different preset\n"
                       "- Clear the input and start fresh\n"
                       "- Check if all required fields are present")
            else:
                st.warning("⚠️ **Unexpected Error**")
                st.info("💡 **Try:**\n"
                       "- Refresh the page\n"
                       "- Check your input format\n"
                       "- Try with a simpler diagram first")
            
            # Technical details in expander
            with st.expander("🔍 **Technical Error Details**", expanded=False):
                st.exception(e)
                st.code(f"Error Type: {error_type}\nError Message: {error_msg}", language="text")
    else: 
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%); padding: 2rem; border-radius: 12px; border: 2px solid #4facfe; margin: 2rem 0;">
            <h3 style="color: #4facfe; text-align: center; margin-bottom: 1rem;">📝 Get Started</h3>
            <p style="text-align: center; color: #667eea; font-size: 1.1rem; margin-bottom: 1.5rem;">
                Enter text in the left panel to generate a diagram. Try a preset or create your own!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #667eea; margin: 1rem 0;">
            <h4 style="color: #667eea; margin-top: 0;">📖 Syntax Guide:</h4>
            <ul style="color: #764ba2; line-height: 1.8;">
                <li>Use <code style="background: rgba(102, 126, 234, 0.2); padding: 2px 6px; border-radius: 4px;">#</code> for section/cluster titles</li>
                <li>Use <code style="background: rgba(102, 126, 234, 0.2); padding: 2px 6px; border-radius: 4px;">→</code> or <code style="background: rgba(102, 126, 234, 0.2); padding: 2px 6px; border-radius: 4px;">-></code> or <code style="background: rgba(102, 126, 234, 0.2); padding: 2px 6px; border-radius: 4px;">=></code> for horizontal connections</li>
                <li>Use <code style="background: rgba(102, 126, 234, 0.2); padding: 2px 6px; border-radius: 4px;">↓</code> or <code style="background: rgba(102, 126, 234, 0.2); padding: 2px 6px; border-radius: 4px;">v</code> or <code style="background: rgba(102, 126, 234, 0.2); padding: 2px 6px; border-radius: 4px;">|</code> for vertical connections</li>
                <li>Add edge labels with <code style="background: rgba(102, 126, 234, 0.2); padding: 2px 6px; border-radius: 4px;">[label]</code> on arrows</li>
                <li><strong>Example:</strong> <code style="background: rgba(102, 126, 234, 0.2); padding: 2px 6px; border-radius: 4px;">Node A [GET] → Node B → Node C</code></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Download Sample Format and Conversion Manual
        st.markdown("---")
        st.markdown("### 📚 Help & Resources")
        
        col_help1, col_help2 = st.columns(2, gap="medium")
        
        with col_help1:
            # Read sample format file
            try:
                with open("sample_diagram_format.txt", "r", encoding="utf-8") as f:
                    sample_format_content = f.read()
                st.download_button(
                    "📄 Download Sample Format File",
                    sample_format_content,
                    "sample_diagram_format.txt",
                    "text/plain",
                    use_container_width=True,
                    help="Download a template file with examples of the correct format. Use this as a starting point for your diagrams."
                )
            except FileNotFoundError:
                st.warning("⚠️ Sample format file not found. Please ensure 'sample_diagram_format.txt' exists in the same directory.")
        
        with col_help2:
            # Read conversion manual
            try:
                with open("CONVERSION_MANUAL.md", "r", encoding="utf-8") as f:
                    manual_content = f.read()
                st.download_button(
                    "📘 Download Conversion Manual",
                    manual_content,
                    "CONVERSION_MANUAL.md",
                    "text/markdown",
                    use_container_width=True,
                    help="Download the complete manual explaining how to convert your existing text documents into the diagram format. Perfect for VS Code workflow!"
                )
            except FileNotFoundError:
                st.warning("⚠️ Conversion manual not found. Please ensure 'CONVERSION_MANUAL.md' exists in the same directory.")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%); padding: 1.5rem; border-radius: 12px; border: 2px solid #4facfe; margin: 1rem 0;">
            <h4 style="color: #4facfe; margin-top: 0;">💡 How to Convert Your Text:</h4>
            <ol style="color: #667eea; line-height: 2;">
                <li><strong>Download</strong> the Sample Format File and Conversion Manual above</li>
                <li><strong>Open VS Code</strong> and open your source file</li>
                <li><strong>Open the Conversion Manual</strong> in VS Code (split view)</li>
                <li><strong>Follow the manual</strong> to convert your text into the format</li>
                <li><strong>Copy the converted text</strong> and paste it here to generate your diagram!</li>
            </ol>
            <p style="color: #764ba2; margin-top: 1rem; font-size: 0.95rem;">
                <strong>💻 VS Code Tip:</strong> Use Find & Replace (Ctrl+H / Cmd+H) for bulk conversions like replacing "then" with "→"
            </p>
        </div>
        """, unsafe_allow_html=True)