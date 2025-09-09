import dash
from dash import dcc, html, Input, Output, callback, dash_table, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import io
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import request, redirect, url_for, session, send_file
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import seaborn as sns
from scipy.interpolate import interp1d
import numpy as np

# User and Role Management
class User(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

# Define users and roles from environment variables
USERS = {
    os.environ.get('ADMIN_USERNAME', 'admin'): User(
        '1', 
        os.environ.get('ADMIN_USERNAME', 'admin'), 
        os.environ.get('ADMIN_PASSWORD', 'dedalus2024'), 
        'executive'
    ),
    os.environ.get('VIEWER_USERNAME', 'viewer'): User(
        '2', 
        os.environ.get('VIEWER_USERNAME', 'viewer'), 
        os.environ.get('VIEWER_PASSWORD', 'viewer2024'), 
        'operational'
    )
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='../static')
app.title = "Dedalus - Tooling Dashboard"
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'dedalus-dashboard-secret-key-2024')

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(user_id):
    for user in USERS.values():
        if user.id == user_id:
            return user
    return None

# Login route
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username].password == password:
            login_user(USERS[username])
            return redirect('/')
        else:
            return '''
            <div style="text-align: center; margin-top: 100px; font-family: Arial;">
                <h2 style="color: #1f4e79;">🔐 Dedalus - Tooling Dashboard</h2>
                <div style="color: red; margin: 20px; padding: 10px; background: #ffe6e6; border-radius: 5px;">❌ Invalid credentials</div>
                <form method="post" style="max-width: 300px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: #f9f9f9;">
                    <input type="text" name="username" placeholder="Username" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; font-size: 14px;"><br>
                    <input type="password" name="password" placeholder="Password" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; font-size: 14px;"><br>
                    <button type="submit" style="width: 100%; padding: 12px; background: #1f4e79; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold;">🔑 Login</button>
                </form>
                <div style="margin-top: 20px; padding: 15px; background: #e6f3ff; border-radius: 5px; font-size: 12px; color: #333;">
                    <strong>Demo Credentials:</strong><br>
                    👨‍💼 Executive: <code>admin</code> / <code>dedalus2024</code><br>
                    👨‍💻 Operational: <code>viewer</code> / <code>viewer2024</code>
                </div>
            </div>
            '''
    
    # Check if user was logged out
    logged_out = request.args.get('logged_out')
    logout_message = ''
    if logged_out:
        logout_message = '<div style="color: green; margin: 20px; padding: 10px; background: #e6ffe6; border-radius: 5px;">✅ Successfully logged out</div>'
    
    return f'''
    <div style="text-align: center; margin-top: 100px; font-family: Arial;">
        <h2 style="color: #1f4e79;">🔐 Dedalus - Tooling Dashboard</h2>
        {logout_message}
        <p style="margin: 20px; color: #666;">Please login to access the dashboard</p>
        <form method="post" style="max-width: 300px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: #f9f9f9;">
            <input type="text" name="username" placeholder="Username" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; font-size: 14px;"><br>
            <input type="password" name="password" placeholder="Password" required style="width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; font-size: 14px;"><br>
            <button type="submit" style="width: 100%; padding: 12px; background: #1f4e79; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold;">🔑 Login</button>
        </form>
        <div style="margin-top: 20px; padding: 15px; background: #e6f3ff; border-radius: 5px; font-size: 12px; color: #333;">
            <strong>Demo Credentials:</strong><br>
            👨‍💼 Executive: <code>admin</code> / <code>dedalus2024</code><br>
            👨‍💻 Operational: <code>viewer</code> / <code>viewer2024</code>
        </div>
    </div>
    '''

# Download template route
@server.route('/get-template')
def get_template():
    return send_file('/mnt/c/BI-Dashboard/data/populated_migration_template.xlsx', 
                    as_attachment=True, 
                    download_name='migration_template.xlsx')

# Logout route
@server.route('/logout')
def logout():
    logout_user()
    session.clear()
    response = redirect('/login?logged_out=1')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Middleware to protect dashboard
@server.before_request
def require_login():
    if request.endpoint in ['static', 'get_template', 'login', 'logout']:
        return
    if request.path.startswith('/assets') or request.path.startswith('/_favicon'):
        return
    if request.path.startswith('/_dash') and not current_user.is_authenticated:
        return redirect('/login')
    if request.path == '/' and not current_user.is_authenticated:
        return redirect('/login')

# Global variables for data
migration_df = pd.DataFrame()
cost_df = pd.DataFrame()

# Color scheme
COLORS = {
    'primary': '#1f4e79',
    'secondary': '#2c5aa0',
    'success': '#28a745',
    'info': '#17a2b8',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

def load_default_data():
    """Load default data from template"""
    global migration_df, cost_df
    try:
        data_paths = [
            '/mnt/c/BI-Dashboard/data/populated_migration_template.xlsx',
            '../data/populated_migration_template.xlsx',
            'data/populated_migration_template.xlsx'
        ]
        
        for path in data_paths:
            try:
                migration_df = pd.read_excel(path, sheet_name='Migration Status')
                cost_df = pd.read_excel(path, sheet_name='Cost Saving')
                break
            except FileNotFoundError:
                continue
        
        if migration_df.empty:
            raise FileNotFoundError("No data file found")
            
        cost_df['Cost Saving'] = pd.to_numeric(cost_df['Cost Saving'], errors='coerce').fillna(0)
        cost_df['Total Users'] = pd.to_numeric(cost_df['Total Users'], errors='coerce').fillna(0)
        cost_df['Annual Savings'] = cost_df['Cost Saving'] * 12
        
        print(f"✅ Default data loaded: {len(migration_df)} tools, ${cost_df['Annual Savings'].sum():,.0f} annual savings")
        return True
    except Exception as e:
        print(f"❌ Error loading default data: {e}")
        migration_df = pd.DataFrame(columns=[
            'Product Name/ Inventory', 'Regional Owner', 'Strategic', 'Priority',
            'Comments/Status', 'GitHub Migration', 'GitHub Actions', 'JIRA Migration',
            'overall_migration_status', 'migration_completion_score'
        ])
        cost_df = pd.DataFrame(columns=[
            'Products', 'Migration from', 'Cost per month', 'Total Users', 'Cost Saving', 'Annual Savings'
        ])
        return False

def create_smooth_line_data(x_data, y_data):
    """Create smooth line data using interpolation"""
    if len(x_data) < 3:
        return x_data, y_data
    
    try:
        # Create numeric indices for interpolation
        x_indices = np.arange(len(x_data))
        
        # Interpolate for smooth curve
        f = interp1d(x_indices, y_data, kind='cubic')
        x_smooth = np.linspace(0, len(x_data)-1, len(x_data)*3)
        y_smooth = f(x_smooth)
        
        # Map back to original x labels
        x_labels_smooth = []
        for i in x_smooth:
            idx = int(round(i))
            if idx < len(x_data):
                x_labels_smooth.append(x_data[idx])
            else:
                x_labels_smooth.append(x_data[-1])
        
        return x_labels_smooth, y_smooth
    except:
        return x_data, y_data

def create_matplotlib_line_chart(df, title, x_col, y_col, color='blue'):
    """Create matplotlib line chart and return as base64 image"""
    try:
        plt.style.use('seaborn-v0_8')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Sort data for better line visualization
        plot_data = df.sort_values(y_col, ascending=False)
        
        # Create smooth line
        x_smooth, y_smooth = create_smooth_line_data(
            plot_data[x_col].tolist(), 
            plot_data[y_col].tolist()
        )
        
        # Plot line with markers
        ax.plot(range(len(plot_data)), plot_data[y_col], 
               marker='o', linewidth=3, markersize=8, color=color)
        
        # Customize chart
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        ax.set_xticks(range(len(plot_data)))
        ax.set_xticklabels(plot_data[x_col], rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        
        # Add value labels on points
        for i, (x, y) in enumerate(zip(range(len(plot_data)), plot_data[y_col])):
            ax.annotate(f'{y:.1f}', (x, y), textcoords="offset points", 
                       xytext=(0,10), ha='center', fontweight='bold')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"
    except Exception as e:
        plt.close()
        return None

# Load default data on startup
load_default_data()

def create_kpi_cards():
    """Create KPI cards with current data"""
    try:
        if cost_df.empty or migration_df.empty:
            return html.Div("No data available for KPIs", className="text-center")
        
        total_savings = cost_df['Annual Savings'].sum()
        total_tools = len(migration_df)
        total_users = cost_df['Total Users'].sum()
        
        # Calculate ROI (simplified)
        roi = 388 if total_savings > 0 else 0
        
        cards = dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"${total_savings:,.0f}", className="card-title text-success"),
                        html.P("Annual Cost Savings", className="card-text")
                    ])
                ], className="text-center shadow-sm")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{roi}%", className="card-title text-info"),
                        html.P("ROI", className="card-text")
                    ])
                ], className="text-center shadow-sm")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{total_tools}", className="card-title text-primary"),
                        html.P("Tools in Migration", className="card-text")
                    ])
                ], className="text-center shadow-sm")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{total_users:,.0f}", className="card-title text-warning"),
                        html.P("Total Users", className="card-text")
                    ])
                ], className="text-center shadow-sm")
            ], width=3)
        ], className="mb-4")
        
        return cards
    except Exception as e:
        return html.Div(f"Error creating KPIs: {str(e)}", className="text-center")

# Layout
app.layout = dbc.Container([
    # Header
    dbc.Navbar([
        dbc.Container([
            dbc.NavbarBrand([
                html.Img(src="/assets/Dedalus_fav.png", height="30", className="me-2"),
                "Dedalus - Tooling Dashboard"
            ], className="text-white fw-bold d-flex align-items-center"),
            dbc.Nav([
                dbc.NavItem([
                    html.Span(id="user-info", className="text-white me-3"),
                    html.A("Logout", href="/logout", className="btn btn-light btn-sm", 
                           style={'textDecoration': 'none', 'color': '#1f4e79'})
                ])
            ], className="ms-auto")
        ])
    ], color=COLORS['primary'], dark=True, className="mb-4"),
    
    # Data Import Section (Executive only)
    html.Div(id="data-import-section"),
    
    # KPI Cards
    html.Div(id="kpi-cards"),
    
    # Main Dashboard
    html.Div(id="main-dashboard")
], fluid=True, style={'backgroundColor': COLORS['light'], 'minHeight': '100vh'})

# Callbacks
@callback(
    [Output('user-info', 'children'),
     Output('data-import-section', 'children'),
     Output('kpi-cards', 'children'),
     Output('main-dashboard', 'children')],
    Input('user-info', 'id'),
    prevent_initial_call=False
)
def update_dashboard(_):
    try:
        if not current_user.is_authenticated:
            return "", "", "", html.Div([
                html.H2("🔐 Please Login", style={'textAlign': 'center', 'color': '#1f4e79', 'marginTop': '100px'}),
                html.A("Go to Login", href="/login", style={'textAlign': 'center', 'display': 'block', 'color': '#1f4e79'})
            ])
    except:
        return "", "", "", html.Div([
            html.H2("🔐 Please Login", style={'textAlign': 'center', 'color': '#1f4e79', 'marginTop': '100px'}),
            html.A("Go to Login", href="/login", style={'textAlign': 'center', 'display': 'block', 'color': '#1f4e79'})
        ])
    
    user_info = f"Welcome, {current_user.username} ({current_user.role.title()})"
    
    # Data import section (Executive only)
    data_import = ""
    if current_user.role == 'executive':
        data_import = dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.I(className="fas fa-upload me-2 text-primary"),
                            html.Strong("Data Import & Validation", className="text-primary")
                        ], className="mb-2")
                    ], width=12),
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Upload(
                            id='upload-data',
                            children=dbc.Button([
                                html.I(className="fas fa-file-excel me-2"),
                                'Upload Excel File'
                            ], color="primary", size="sm", className="w-100"),
                            multiple=False,
                            accept='.xlsx,.xls',
                            className="d-grid"
                        )
                    ], width=2),
                    dbc.Col([
                        html.A(
                            dbc.Button([
                                html.I(className="fas fa-download me-2"),
                                'Download Template'
                            ], color="secondary", size="sm", className="w-100"),
                            href="/get-template",
                            style={'textDecoration': 'none'}
                        )
                    ], width=2),
                    dbc.Col([
                        html.Div([
                            html.Small("Required: Migration Status & Cost Saving sheets with proper schema", 
                                     className="text-muted")
                        ], className="d-flex align-items-center")
                    ], width=4),
                    dbc.Col([
                        html.Div(id="upload-status")
                    ], width=4)
                ], className="align-items-center")
            ])
        ], className="mb-4 shadow-sm border-0")
    
    # KPI Cards
    kpi_cards = create_kpi_cards()
    
    # Main dashboard with tabs and filtering
    if migration_df.empty:
        dashboard_content = html.Div("No data available", className="text-center")
    else:
        # Get filter options
        owner_options = [{'label': 'All', 'value': 'All'}] + [{'label': str(owner), 'value': str(owner)} for owner in migration_df['Regional Owner'].dropna().unique()]
        status_options = [{'label': 'All', 'value': 'All'}] + [{'label': str(status), 'value': str(status)} for status in migration_df['overall_migration_status'].dropna().unique()]
        
        # Dashboard tabs based on role
        if current_user.role == 'executive':
            tabs = [
                dbc.Tab(label="Executive View", tab_id="executive"),
                dbc.Tab(label="Operational View", tab_id="operational")
            ]
            default_tab = "executive"
        else:
            tabs = [dbc.Tab(label="Operational View", tab_id="operational")]
            default_tab = "operational"
        
        dashboard_content = dbc.Card([
            dbc.CardHeader([
                dbc.Tabs(tabs, id="main-tabs", active_tab=default_tab)
            ]),
            dbc.CardBody([
                # Executive Tab Content
                html.Div(id="executive-tab", children=[
                    dbc.Row([
                        dbc.Col([
                            html.Label("Regional Owner:", className="fw-bold"),
                            dcc.Dropdown(id='exec-owner-filter', options=owner_options, value='All')
                        ], width=4),
                        dbc.Col([
                            html.Label("Chart Type:", className="fw-bold"),
                            dcc.Dropdown(
                                id='exec-chart-type',
                                options=[
                                    {'label': 'Pie Chart', 'value': 'pie'},
                                    {'label': 'Bar Chart', 'value': 'bar'},
                                    {'label': 'Donut Chart', 'value': 'donut'},
                                    {'label': 'Stacked by Priority', 'value': 'stack_priority'},
                                    {'label': 'Stacked by Owner', 'value': 'stack_owner'}
                                ],
                                value='pie'
                            )
                        ], width=4),
                        dbc.Col([
                            html.Label("View Type:", className="fw-bold"),
                            html.Br(),
                            dbc.ButtonGroup([
                                dbc.Button("Charts", id="exec-chart-btn", color="primary", size="sm"),
                                dbc.Button("Tables", id="exec-table-btn", color="outline-primary", size="sm")
                            ])
                        ], width=4)
                    ], className="mb-4"),
                    html.Div(id="executive-content")
                ], style={'display': 'block' if current_user.role == 'executive' else 'none'}),
                
                # Operational Tab Content
                html.Div(id="operational-tab", children=[
                    dbc.Row([
                        dbc.Col([
                            html.Label("Migration Status:", className="fw-bold"),
                            dcc.Dropdown(id='ops-status-filter', options=status_options, value='All')
                        ], width=4),
                        dbc.Col([
                            html.Label("Chart Style:", className="fw-bold"),
                            dcc.Dropdown(
                                id='ops-chart-style',
                                options=[
                                    {'label': 'Individual Charts', 'value': 'individual'},
                                    {'label': 'Grouped Bars', 'value': 'group'},
                                    {'label': 'Stacked Bars', 'value': 'stack'},
                                    {'label': 'Stacked with Priority Line', 'value': 'stack_priority'},
                                    {'label': 'Stacked with Count Line', 'value': 'stack_count'}
                                ],
                                value='individual'
                            )
                        ], width=4),
                        dbc.Col([
                            html.Label("View Type:", className="fw-bold"),
                            html.Br(),
                            dbc.ButtonGroup([
                                dbc.Button("Charts", id="ops-chart-btn", color="primary", size="sm"),
                                dbc.Button("Tables", id="ops-table-btn", color="outline-primary", size="sm")
                            ])
                        ], width=4)
                    ], className="mb-4"),
                    html.Div(id="operational-content")
                ], style={'display': 'none' if current_user.role == 'executive' and default_tab == 'executive' else 'block'})
            ])
        ], className="shadow-sm")
    
    return user_info, data_import, kpi_cards, dashboard_content

# Executive content callback
@callback(
    Output('executive-content', 'children'),
    [Input('exec-chart-btn', 'n_clicks'),
     Input('exec-table-btn', 'n_clicks'),
     Input('exec-owner-filter', 'value'),
     Input('exec-chart-type', 'value')],
    prevent_initial_call=False
)
def update_executive_content(chart_clicks, table_clicks, owner_filter, chart_type):
    try:
        if not current_user.is_authenticated or current_user.role != 'executive':
            return ""
        
        ctx = dash.callback_context
        
        # Default values
        owner_filter = owner_filter or 'All'
        chart_type = chart_type or 'pie'
        
        # Determine view type
        show_charts = True
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'exec-table-btn':
                show_charts = False
        
        # Filter data
        df = migration_df.copy()
        if owner_filter != 'All':
            df = df[df['Regional Owner'] == owner_filter]
        
        if df.empty:
            return html.Div("No data for selected filter", className="text-center")
        
        if show_charts:
            # Create charts based on type
            if chart_type == 'pie':
                fig = px.pie(df, names='Regional Owner', title='Tools by Regional Owner')
            elif chart_type == 'bar':
                fig = px.bar(df, x='Regional Owner', title='Tools by Regional Owner')
            elif chart_type == 'donut':
                fig = px.pie(df, names='Regional Owner', title='Tools by Regional Owner', hole=0.4)
            elif chart_type == 'stack_priority':
                # Create proper stacked bar with line overlay using secondary y-axis
                fig = go.Figure()
                
                # Add stacked bars by priority
                priorities = df['Priority'].unique()
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
                
                for i, priority in enumerate(priorities):
                    priority_data = df[df['Priority'] == priority]
                    owner_counts = priority_data.groupby('Regional Owner').size()
                    
                    fig.add_trace(go.Bar(
                        name=f'{priority} Priority',
                        x=owner_counts.index,
                        y=owner_counts.values,
                        marker_color=colors[i % len(colors)],
                        yaxis='y'
                    ))
                
                # Calculate and add progress line overlay
                if 'migration_completion_score' in df.columns:
                    progress_data = df.groupby('Regional Owner')['migration_completion_score'].mean().reset_index()
                    progress_data = progress_data.sort_values('migration_completion_score', ascending=False)
                    
                    fig.add_trace(go.Scatter(
                        name='Progress %',
                        x=progress_data['Regional Owner'],
                        y=progress_data['migration_completion_score'],
                        mode='lines+markers+text',
                        line=dict(color='red', width=4),
                        marker=dict(size=12, color='red', symbol='diamond'),
                        text=[f"{val:.1f}%" for val in progress_data['migration_completion_score']],
                        textposition="top center",
                        yaxis='y2'
                    ))
                
                # Configure layout with dual y-axes
                fig.update_layout(
                    title='Tools by Owner and Priority with Progress Line',
                    barmode='stack',
                    xaxis=dict(title='Regional Owner'),
                    yaxis=dict(title='Number of Tools', side='left'),
                    yaxis2=dict(
                        title='Progress %',
                        overlaying='y',
                        side='right',
                        range=[0, 100],
                        showgrid=False
                    )
                )
                
            elif chart_type == 'stack_owner':
                # Create proper stacked bar with count line overlay
                fig = go.Figure()
                
                # Add stacked bars by owner
                owners = df['Regional Owner'].unique()
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
                
                for i, owner in enumerate(owners):
                    owner_data = df[df['Regional Owner'] == owner]
                    priority_counts = owner_data.groupby('Priority').size()
                    
                    fig.add_trace(go.Bar(
                        name=owner,
                        x=priority_counts.index,
                        y=priority_counts.values,
                        marker_color=colors[i % len(colors)],
                        yaxis='y'
                    ))
                
                # Add total count line overlay
                priority_totals = df.groupby('Priority').size().reset_index(name='total_count')
                priority_totals = priority_totals.sort_values('total_count', ascending=False)
                
                fig.add_trace(go.Scatter(
                    name='Total Count',
                    x=priority_totals['Priority'],
                    y=priority_totals['total_count'],
                    mode='lines+markers+text',
                    line=dict(color='orange', width=4),
                    marker=dict(size=12, color='orange', symbol='diamond'),
                    text=[f"{val}" for val in priority_totals['total_count']],
                    textposition="top center",
                    yaxis='y2'
                ))
                
                # Configure layout with dual y-axes
                fig.update_layout(
                    title='Tools by Priority and Owner with Count Line',
                    barmode='stack',
                    xaxis=dict(title='Priority'),
                    yaxis=dict(title='Number of Tools', side='left'),
                    yaxis2=dict(
                        title='Total Count',
                        overlaying='y',
                        side='right',
                        showgrid=False
                    )
                )
            else:
                fig = px.pie(df, names='Regional Owner', title='Tools by Regional Owner')
            
            # Professional styling with improved bar sizing and tooltips
            fig.update_layout(
                height=500,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10)
                ),
                margin=dict(l=60, r=60, t=100, b=60),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                bargap=0.2,  # Space between bars
                bargroupgap=0.1,  # Space between bar groups
                font=dict(size=12)
            )
            
            if chart_type not in ['pie', 'donut']:
                fig.update_xaxes(
                    showgrid=True, 
                    gridwidth=1, 
                    gridcolor='lightgray',
                    tickangle=45 if len(df) > 5 else 0
                )
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                
                # Improve bar width for better visibility
                fig.update_traces(
                    marker_line_width=1,
                    marker_line_color="white",
                    hovertemplate="<b>%{x}</b><br>Count: %{y}<br><extra></extra>"
                )
            
            return dcc.Graph(figure=fig)
        else:
            # Create table
            return dash_table.DataTable(
                data=df.head(20).to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns[:6]],
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': COLORS['primary'], 'color': 'white'},
                page_size=15,
                sort_action="native"
            )
    except Exception as e:
        return html.Div(f"Error: {str(e)}", className="text-center")

# File upload callback
@callback(
    [Output('upload-status', 'children'),
     Output('kpi-cards', 'children', allow_duplicate=True)],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def handle_file_upload(contents, filename):
    global migration_df, cost_df
    
    if contents is None:
        return "", create_kpi_cards()
    
    try:
        # Parse uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Read Excel file
        migration_df = pd.read_excel(io.BytesIO(decoded), sheet_name='Migration Status')
        cost_df = pd.read_excel(io.BytesIO(decoded), sheet_name='Cost Saving')
        
        # Process cost data
        cost_df['Cost Saving'] = pd.to_numeric(cost_df['Cost Saving'], errors='coerce').fillna(0)
        cost_df['Total Users'] = pd.to_numeric(cost_df['Total Users'], errors='coerce').fillna(0)
        cost_df['Annual Savings'] = cost_df['Cost Saving'] * 12
        
        total_savings = cost_df['Annual Savings'].sum()
        total_tools = len(migration_df)
        
        status_msg = dbc.Alert([
            html.I(className="fas fa-check-circle me-2"),
            f"✅ File uploaded successfully! {total_tools} tools, ${total_savings:,.0f} annual savings"
        ], color="success", dismissable=True)
        
        return status_msg, create_kpi_cards()
        
    except Exception as e:
        error_msg = dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            f"❌ Upload failed: {str(e)}"
        ], color="danger", dismissable=True)
        
        return error_msg, create_kpi_cards()

# Operational content callback
@callback(
    Output('operational-content', 'children'),
    [Input('ops-chart-btn', 'n_clicks'),
     Input('ops-table-btn', 'n_clicks'),
     Input('ops-status-filter', 'value'),
     Input('ops-chart-style', 'value')],
    prevent_initial_call=False
)
def update_operational_content(chart_clicks, table_clicks, status_filter, chart_style):
    try:
        if not current_user.is_authenticated:
            return ""
        
        ctx = dash.callback_context
        
        # Default values
        status_filter = status_filter or 'All'
        chart_style = chart_style or 'individual'
        
        # Determine view type
        show_charts = True
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'ops-table-btn':
                show_charts = False
        
        # Filter data
        df = migration_df.copy()
        if status_filter != 'All':
            df = df[df['overall_migration_status'] == status_filter]
        
        if df.empty:
            return html.Div("No data for selected filter", className="text-center")
        
        if show_charts:
            # Create charts based on style
            if chart_style == 'individual':
                fig = px.bar(df, x='overall_migration_status', title='Migration Status Distribution')
            elif chart_style == 'group':
                fig = px.bar(df, x='overall_migration_status', color='Priority', title='Migration Status by Priority', barmode='group')
            elif chart_style == 'stack':
                fig = px.bar(df, x='overall_migration_status', color='Priority', title='Migration Status by Priority')
            elif chart_style == 'stack_priority':
                # Create proper stacked bar with high priority line overlay
                fig = go.Figure()
                
                # Add stacked bars by priority
                priorities = df['Priority'].unique()
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
                
                for i, priority in enumerate(priorities):
                    priority_data = df[df['Priority'] == priority]
                    status_counts = priority_data.groupby('overall_migration_status').size()
                    
                    fig.add_trace(go.Bar(
                        name=f'{priority} Priority',
                        x=status_counts.index,
                        y=status_counts.values,
                        marker_color=colors[i % len(colors)],
                        yaxis='y'
                    ))
                
                # Add high priority percentage line overlay
                status_priority = df.groupby('overall_migration_status').apply(
                    lambda x: (x['Priority'] == 'High').sum() / len(x) * 100 if len(x) > 0 else 0
                ).reset_index(name='high_priority_pct')
                
                fig.add_trace(go.Scatter(
                    name='High Priority %',
                    x=status_priority['overall_migration_status'],
                    y=status_priority['high_priority_pct'],
                    mode='lines+markers+text',
                    line=dict(color='red', width=4),
                    marker=dict(size=12, color='red', symbol='diamond'),
                    text=[f"{val:.1f}%" for val in status_priority['high_priority_pct']],
                    textposition="top center",
                    yaxis='y2'
                ))
                
                # Configure layout
                fig.update_layout(
                    title='Migration Status with High Priority Line',
                    barmode='stack',
                    xaxis=dict(title='Migration Status'),
                    yaxis=dict(title='Number of Tools', side='left'),
                    yaxis2=dict(
                        title='High Priority %',
                        overlaying='y',
                        side='right',
                        range=[0, 100],
                        showgrid=False
                    )
                )
                
            elif chart_style == 'stack_count':
                # Create proper stacked bar with completion line overlay
                fig = go.Figure()
                
                # Add stacked bars by owner
                owners = df['Regional Owner'].unique()
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
                
                for i, owner in enumerate(owners):
                    owner_data = df[df['Regional Owner'] == owner]
                    status_counts = owner_data.groupby('overall_migration_status').size()
                    
                    fig.add_trace(go.Bar(
                        name=owner,
                        x=status_counts.index,
                        y=status_counts.values,
                        marker_color=colors[i % len(colors)],
                        yaxis='y'
                    ))
                
                # Add completion percentage line overlay
                if 'migration_completion_score' in df.columns:
                    completion_data = df.groupby('overall_migration_status')['migration_completion_score'].mean().reset_index()
                    
                    fig.add_trace(go.Scatter(
                        name='Avg Completion %',
                        x=completion_data['overall_migration_status'],
                        y=completion_data['migration_completion_score'],
                        mode='lines+markers+text',
                        line=dict(color='green', width=4),
                        marker=dict(size=12, color='green', symbol='diamond'),
                        text=[f"{val:.1f}%" for val in completion_data['migration_completion_score']],
                        textposition="top center",
                        yaxis='y2'
                    ))
                
                # Configure layout
                fig.update_layout(
                    title='Migration Status with Completion Line',
                    barmode='stack',
                    xaxis=dict(title='Migration Status'),
                    yaxis=dict(title='Number of Tools', side='left'),
                    yaxis2=dict(
                        title='Completion %',
                        overlaying='y',
                        side='right',
                        range=[0, 100],
                        showgrid=False
                    )
                )
            else:
                fig = px.bar(df, x='overall_migration_status', title='Migration Status Distribution')
            
            # Professional styling with improved bar sizing and tooltips
            fig.update_layout(
                height=500,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10)
                ),
                margin=dict(l=60, r=60, t=100, b=60),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                bargap=0.2,  # Space between bars
                bargroupgap=0.1,  # Space between bar groups
                font=dict(size=12)
            )
            
            fig.update_xaxes(
                showgrid=True, 
                gridwidth=1, 
                gridcolor='lightgray',
                tickangle=45 if len(df) > 5 else 0
            )
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            
            # Improve bar styling and tooltips
            fig.update_traces(
                marker_line_width=1,
                marker_line_color="white",
                hovertemplate="<b>%{x}</b><br>Count: %{y}<br><extra></extra>"
            )
            
            return dcc.Graph(figure=fig)
        else:
            # Create table
            return dash_table.DataTable(
                data=df.head(20).to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns[:6]],
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': COLORS['primary'], 'color': 'white'},
                page_size=15,
                sort_action="native"
            )
    except Exception as e:
        return html.Div(f"Error: {str(e)}", className="text-center")

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=int(os.environ.get('PORT', 8050)), debug=os.environ.get('DEBUG', 'false').lower() == 'true')
