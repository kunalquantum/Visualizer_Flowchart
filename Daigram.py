import streamlit as st
import streamlit.components.v1 as components
import re
import html
import base64
import json
import graphviz
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="CloudDMate Architecture",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Icon Logic ---
def add_icons(label):
    """Injects icons based on keywords to make diagrams visual."""
    l = label.lower()
    prefix = ""
    if any(x in l for x in ["user", "actor", "client", "customer"]): prefix = "👤 "
    elif any(x in l for x in ["db", "data", "sql", "store", "oracle"]): prefix = "🛢️ "
    elif any(x in l for x in ["cloud", "aws", "azure"]): prefix = "☁️ "
    elif any(x in l for x in ["api", "rest", "json", "endpoint"]): prefix = "🔌 "
    elif any(x in l for x in ["lock", "auth", "login", "security"]): prefix = "🔒 "
    elif any(x in l for x in ["email", "message", "notification"]): prefix = "📧 "
    elif any(x in l for x in ["error", "fail", "404", "500"]): prefix = "⚠️ "
    elif any(x in l for x in ["settings", "config", "setup"]): prefix = "⚙️ "
    elif any(x in l for x in ["file", "upload", "excel", "csv"]): prefix = "📄 "
    elif any(x in l for x in ["check", "validate", "success", "ok"]): prefix = "✅ "
    elif any(x in l for x in ["web", "site", "dashboard", "ui"]): prefix = "🖥️ "
    elif any(x in l for x in ["mobile", "app", "phone"]): prefix = "📱 "
    
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

def get_graphviz_style(label, theme_name):
    theme = THEMES[theme_name]
    node_type = get_node_type(label)
    style_config = theme["types"].get(node_type, theme["default"])
    base_config = theme["default"].copy()
    base_config.update(style_config)
    s = base_config
    return f'shape="{s["shape"]}", style="{s.get("style", "filled")}", fillcolor="{s["fill"]}", color="{s["border"]}", fontcolor="{s["text"]}"'

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
    lines = text.split('\n')
    clusters = [] 
    nodes = {}    
    edges = []    
    current_cluster = None
    cluster_counter = 0
    last_node_id_of_prev_line = None
    connect_next_line = False
    arrow_split_re = r'\s*(?:→|->|=>)\s*'
    
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
            
        parts = re.split(arrow_split_re, line)
        row_node_ids = []
        
        for part in parts:
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
            edges.append((last_node_id_of_prev_line, row_node_ids[0]))
            connect_next_line = False
        
        for i in range(len(row_node_ids) - 1):
            edges.append((row_node_ids[i], row_node_ids[i+1]))
            
        last_node_id_of_prev_line = row_node_ids[-1]

    return nodes, edges, clusters

def generate_dot_code(nodes, edges, clusters, theme_name, layout_engine="dot", splines="ortho"):
    """
    Generate Graphviz DOT code.
    """
    theme = THEMES[theme_name]
    
    engine_map = {
        "Hierarchy (Waterfall)": "dot",
        "Organic (Force)": "neato",
        "Circular (Ring)": "circo",
        "Radial (Star)": "twopi",
        "Freeform": "fdp"
    }
    engine = engine_map.get(layout_engine, "dot")
    
    rankdir_str = 'rankdir=TB;' if engine == 'dot' else ''
    splines_val = 'curved' if engine in ['neato', 'fdp'] else splines
    
    # SVG Optimization: No forced size, no DPI (vectors don't have pixels)
    dot = [
        'digraph G {',
        f'  layout={engine};',
        f'  {rankdir_str}',
        f'  bgcolor="transparent";',
        f'  splines={splines_val};',
        '  overlap=false;',  
        '  nodesep=0.6;',
        '  ranksep=0.8;',
        f'  node [fontname="{theme["font"]}", fontsize=10, penwidth=1.5];',
        f'  edge [fontname="{theme["font"]}", fontsize=9, color="{theme["edge_color"]}", arrowsize=0.8];'
    ]
    
    def escape_label(s): return s.replace('"', '\\"')
    
    rendered_nodes = set()
    
    use_clusters = engine in ['dot', 'fdp']
    
    if use_clusters:
        for c in clusters:
            dot.append(f'  subgraph {c["id"]} {{')
            dot.append(f'    label="{escape_label(c["title"])}";')
            dot.append(f'    style="rounded,dashed";')
            dot.append(f'    color="{theme["edge_color"]}";')
            dot.append(f'    fontcolor="{theme["edge_color"]}";')
            
            for nid in c['nodes']:
                if nid in nodes:
                    style = get_graphviz_style(nodes[nid], theme_name)
                    dot.append(f'    {nid} [label="{escape_label(nodes[nid])}", {style}];')
                    rendered_nodes.add(nid)
            dot.append('  }')
            
    for nid, label in nodes.items():
        if not use_clusters or nid not in rendered_nodes:
            style = get_graphviz_style(label, theme_name)
            dot.append(f'    {nid} [label="{escape_label(label)}", {style}];')
            
    for src, dst in edges:
        dot.append(f'    {src} -> {dst};')
        
    dot.append('}')
    return "\n".join(dot)

def generate_drawio_xml(nodes, edges, clusters):
    xml = [
        '<mxfile host="app.diagrams.net" modified="2024-01-01T00:00:00.000Z" agent="CloudDMate" version="21.0.0" type="device">',
        '  <diagram id="C5RBs43oDa-KdzZeNtuy" name="Architecture">',
        '    <mxGraphModel dx="0" dy="0" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">',
        '      <root>',
        '        <mxCell id="0" />',
        '        <mxCell id="1" parent="0" />'
    ]
    x, y = 40, 40
    for nid, label in nodes.items():
        style = get_drawio_style(label)
        xml.append(f'        <mxCell id="{nid}" value="{html.escape(label)}" style="{style}" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="{x}" y="{y}" width="160" height="60" as="geometry" />')
        xml.append('        </mxCell>')
        y += 100
        if y > 1000:
            y = 40
            x += 220
    edge_id = 10000
    for src, dst in edges:
        xml.append(f'        <mxCell id="{edge_id}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="{src}" target="{dst}">')
        xml.append('          <mxGeometry relative="1" as="geometry" />')
        xml.append('        </mxCell>')
        edge_id += 1
    xml.append('      </root></mxGraphModel></diagram></mxfile>')
    return "\n".join(xml)

def render_drawio_editor(xml_content):
    json_xml = json.dumps(xml_content)
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body, html {{ margin: 0; padding: 0; height: 100%; overflow: hidden; background: #f0f0f0; }}
            #drawio-iframe {{ width: 100%; height: 100%; border: none; }}
            #controls {{ position: absolute; top: 10px; right: 10px; z-index: 1000; }}
            button {{ 
                background: #336699; color: white; border: none; padding: 8px 12px; 
                border-radius: 4px; cursor: pointer; font-family: sans-serif; font-size: 12px;
                opacity: 0.8; transition: opacity 0.2s;
            }}
            button:hover {{ opacity: 1; }}
        </style>
    </head>
    <body>
        <div id="controls"><button onclick="loadDiagram()">Reload Diagram</button></div>
        <iframe id="drawio-iframe" src="https://embed.diagrams.net/?embed=1&ui=min&spin=1&proto=json&configure=1&grid=1"></iframe>
        <script>
            var iframe = document.getElementById('drawio-iframe');
            var xml = {json_xml};
            var isLoaded = false;
            function loadDiagram() {{
                if (iframe && iframe.contentWindow) {{
                    iframe.contentWindow.postMessage(JSON.stringify({{ action: 'load', xml: xml, autosave: 0 }}), '*');
                    isLoaded = true;
                }}
            }}
            window.addEventListener('message', function(event) {{
                if (event.data.length > 0) {{
                    try {{
                        var msg = JSON.parse(event.data);
                        if (msg.event == 'init') loadDiagram();
                    }} catch (e) {{}}
                }}
            }});
            setTimeout(function() {{ if (!isLoaded) loadDiagram(); }}, 2000);
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=700)

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
}

# --- Sidebar ---
st.sidebar.title("🏗️ Auto-Architect")
st.sidebar.markdown("Convert text flows into innovative visual systems.")

selected_preset = st.sidebar.selectbox("Load Preset", list(PRESETS.keys()))

st.sidebar.divider()
st.sidebar.subheader("🎨 Styling & Layout")

selected_theme = st.sidebar.selectbox("Visual Theme", list(THEMES.keys()), index=0)
layout_engine = st.sidebar.selectbox("Layout Structure", 
    ["Hierarchy (Waterfall)", "Organic (Force)", "Circular (Ring)", "Radial (Star)", "Freeform"],
    help="Change the fundamental shape of the diagram."
)
splines = st.sidebar.selectbox("Line Style", ["ortho", "curved", "polyline"])

st.sidebar.divider()
st.sidebar.info("Tip: Icons are automatically added based on keywords like 'Cloud', 'DB', 'User'.")

# --- Main UI ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📝 Input")
    if "text_input" not in st.session_state: st.session_state.text_input = PRESETS[selected_preset]
    if "last_preset" not in st.session_state or st.session_state.last_preset != selected_preset:
        st.session_state.text_input = PRESETS[selected_preset]
        st.session_state.last_preset = selected_preset
    user_text = st.text_area("Paste flows:", value=st.session_state.text_input, height=600, key="main_input")

with col2:
    st.subheader("✨ Visual System")
    if user_text:
        try:
            nodes, edges, clusters = parse_diagram_data(user_text)
            
            # Generate DOT without constraints for SVG
            dot_code = generate_dot_code(nodes, edges, clusters, selected_theme, layout_engine, splines)
            drawio_xml = generate_drawio_xml(nodes, edges, clusters)
            
            tab1, tab2 = st.tabs(["📊 Smart View", "✏️ Visual Editor"])
            with tab1:
                png_data = None

                # 1. Fetch Responsive SVG for Screen
                # This guarantees clarity and no overflow
                try:
                    resp_svg = requests.post(
                        "https://quickchart.io/graphviz", 
                        json={"graph": dot_code, "format": "svg"}, 
                        timeout=15
                    )
                    
                    if resp_svg.status_code == 200:
                        svg_code = resp_svg.text
                        # Fix: Make SVG Responsive by removing fixed width/height
                        svg_code = re.sub(r'width=".*?"', 'width="100%"', svg_code, count=1)
                        svg_code = re.sub(r'height=".*?"', '', svg_code, count=1)
                        
                        # Wrap in scroll container just in case, but force width
                        # FIXED: HTML indentation removed to prevent markdown code block rendering
                        st.markdown(f"""<div style="width: 100%; overflow-x: auto; border: 1px solid #eee; border-radius: 8px; padding: 10px;">{svg_code}</div>""", unsafe_allow_html=True)
                        
                        # 2. Fetch High-Res PNG for Download Only
                        try:
                            # Add DPI for download version
                            dot_code_dl = dot_code.replace('graph {', 'graph { dpi=300; ')
                            resp_png = requests.post(
                                "https://quickchart.io/graphviz", 
                                json={"graph": dot_code_dl, "format": "png"}, 
                                timeout=15
                            )
                            if resp_png.status_code == 200:
                                png_data = resp_png.content
                        except: pass
                        
                    else:
                        st.error(f"Visualization service busy. Status: {resp_svg.status_code}")
                except Exception as e:
                    st.error(f"Visualizer Connection Issue: {e}")

                st.divider()
                
                c1, c2, c3 = st.columns(3)
                with c1: st.download_button("Download .drawio", drawio_xml, "arch.drawio", "application/xml")
                with c2: 
                    if png_data: st.download_button("Download PNG (High Res)", png_data, "arch.png", "image/png")
                    else: st.info("PNG Generating...")
                with c3:
                    with st.expander("View DOT"): st.code(dot_code, language="dot")

            with tab2:
                st.info("Edit your system map visually.")
                render_drawio_editor(drawio_xml)
        except Exception as e: st.error(f"Error: {e}")
    else: st.info("Enter text.")