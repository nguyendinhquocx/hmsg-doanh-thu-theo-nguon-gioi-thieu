import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Cấu hình trang
st.set_page_config(
    page_title="Phân tíchdoanh thutheo Nguồn Giới thiệu",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"    
)

# CSS tùy chỉnh
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1f77b4;
}
.sidebar-header {
    font-size: 1.2rem;
    font-weight: bold;
    color: #1f77b4;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Hàm đọc và xử lý dữ liệu
@st.cache_data
def load_data():
    try:
        # Đọc dữ liệu từ file Excel
        df = pd.read_excel('file xu li du lieu.xlsx', sheet_name='table')
        
        # Làm sạch tên cột
        df.columns = df.columns.str.strip()
        
        # Kiểm tra và xử lý dữ liệu thiếu
        df = df.dropna()
        
        return df
    except FileNotFoundError:
        st.error("Không tìm thấy file 'file xu li du lieu.xlsx'. Vui lòng đảm bảo file tồn tại trong thư mục hiện tại.")
        return None
    except Exception as e:
        st.error(f"Lỗi khi đọc dữ liệu: {str(e)}")
        return None

# Hàm tính toán các chỉ số
def calculate_metrics(df):
    # Tổng hợp theo nguồn giới thiệu
    doanh_thu_theo_nguon = df.groupby('noi gioi thieu').agg({
        'doanh thu': 'sum',
        'so luong': 'sum'
    }).sort_values('doanh thu', ascending=False)
    
    # Tổng hợp theo tháng
    doanh_thu_theo_thang = df.groupby('thang').agg({
        'doanh thu': 'sum',
        'so luong': 'sum'
    })
    
    # Hiệu suất nguồn (doanh thu trung bình mỗi lượt)
    hieu_suat_nguon = doanh_thu_theo_nguon.copy()
    hieu_suat_nguon['trung binh'] = hieu_suat_nguon['doanh thu'] / hieu_suat_nguon['so luong']
    hieu_suat_nguon = hieu_suat_nguon.sort_values('trung binh', ascending=False)
    
    # Pivot table cho heatmap
    pivot_doanh_thu = df.pivot_table(
        values='doanh thu',
        index='noi gioi thieu',
        columns='thang',
        aggfunc='sum',
        fill_value=0
    )
    
    return doanh_thu_theo_nguon, doanh_thu_theo_thang, hieu_suat_nguon, pivot_doanh_thu

# Hàm tạo biểu đồ
def create_charts(df, doanh_thu_theo_nguon, doanh_thu_theo_thang, hieu_suat_nguon, pivot_doanh_thu, selected_sources, selected_months):
    
    # Lọc dữ liệu theo lựa chọn
    filtered_df = df[
        (df['noi gioi thieu'].isin(selected_sources)) & 
        (df['thang'].isin(selected_months))
    ]
    
    # 1. Biểu đồ cột Top nguồn giới thiệu
    top_sources = doanh_thu_theo_nguon.head(10)
    fig1 = px.bar(
        x=top_sources.index,
        y=top_sources['doanh thu'],
        title="Top 10 Nguồn Giới thiệu theo Doanh thu",
        labels={'x': 'Nguồn Giới thiệu', 'y': 'Doanh thu (VNĐ)'},
        color=top_sources['doanh thu'],
        color_continuous_scale='Blues'
    )
    fig1.update_layout(xaxis_tickangle=-45, height=500)
    fig1.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    
    # 2. Biểu đồ tròn phân bốdoanh thuTop 5
    top5_sources = doanh_thu_theo_nguon.head(5)
    fig2 = px.pie(
        values=top5_sources['doanh thu'],
        names=top5_sources.index,
        title="Phân bốdoanh thuTop 5 Nguồn Giới thiệu"
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    
    # 3. Xu hướngdoanh thutheo tháng
    fig3 = px.line(
        x=doanh_thu_theo_thang.index,
        y=doanh_thu_theo_thang['doanh thu'],
        title="Xu hướngdoanh thutheo Tháng",
        labels={'x': 'Tháng', 'y': 'Doanh thu (VNĐ)'},
        markers=True
    )
    fig3.update_layout(height=400)
    
    # 4. Heatmap doanh thu
    top10_pivot = pivot_doanh_thu.loc[doanh_thu_theo_nguon.head(10).index]
    fig4 = px.imshow(
        top10_pivot.values,
        x=top10_pivot.columns,
        y=top10_pivot.index,
        title="Heatmapdoanh thutheo Nguồn Giới thiệu và Tháng (Top 10)",
        color_continuous_scale='Blues',
        aspect='auto'
    )
    fig4.update_layout(height=600)
    
    # 5. Scatter plot hiệu suất
    filtered_hieu_suat = hieu_suat_nguon[hieu_suat_nguon['so luong'] >= 5]
    fig5 = px.scatter(
        x=filtered_hieu_suat['so luong'],
        y=filtered_hieu_suat['trung binh'],
        hover_name=filtered_hieu_suat.index,
        title="Mối quan hệ giữa Số lượng vàdoanh thuTB/lượt (≥5 lượt)",
        labels={'x': 'Tổng số lượng', 'y': 'Doanh thu trung bình mỗi lượt (VNĐ)'},
        size=filtered_hieu_suat['doanh thu'],
        color=filtered_hieu_suat['trung binh'],
        color_continuous_scale='Viridis'
    )
    fig5.update_layout(height=500)
    
    # 6. Xu hướng Top 5 nguồn theo tháng
    top_5_sources = doanh_thu_theo_nguon.head(5).index
    pivot_for_line = df[df['noi gioi thieu'].isin(top_5_sources)].pivot_table(
        values='doanh thu',
        index='thang',
        columns='noi gioi thieu',
        aggfunc='sum',
        fill_value=0
    )
    
    fig6 = go.Figure()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    for i, source in enumerate(top_5_sources):
        if source in pivot_for_line.columns:
            short_name = source[:30] + '...' if len(source) > 30 else source
            fig6.add_trace(go.Scatter(
                x=pivot_for_line.index,
                y=pivot_for_line[source],
                mode='lines+markers',
                name=short_name,
                line=dict(color=colors[i], width=3),
                marker=dict(size=8)
            ))
    
    fig6.update_layout(
        title="Xu hướngdoanh thuTop 5 Nguồn Giới thiệu theo Tháng",
        xaxis_title="Tháng",
        yaxis_title="Doanh thu (VNĐ)",
        height=500,
        hovermode='x unified'
    )
    
    return fig1, fig2, fig3, fig4, fig5, fig6

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Phân tíchdoanh thutheo Nguồn Giới thiệu</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar filters
    st.sidebar.markdown('<div class="sidebar-header">🔧 Bộ lọc dữ liệu</div>', unsafe_allow_html=True)
    
    # Filter by source
    all_sources = df['noi gioi thieu'].unique().tolist()
    selected_sources = st.sidebar.multiselect(
        "Chọn nguồn giới thiệu:",
        options=all_sources,
        default=all_sources
    )
    
    # Filter by month
    all_months = sorted(df['thang'].unique().tolist())
    selected_months = st.sidebar.multiselect(
        "Chọn tháng:",
        options=all_months,
        default=all_months
    )
    
    # Calculate metrics
    doanh_thu_theo_nguon, doanh_thu_theo_thang, hieu_suat_nguon, pivot_doanh_thu = calculate_metrics(df)
    
    # Filter data for metrics
    filtered_df = df[
        (df['noi gioi thieu'].isin(selected_sources)) & 
        (df['thang'].isin(selected_months))
    ]
    
    # Display key metrics
    st.markdown("## 📈 Tổng quan")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = filtered_df['doanh thu'].sum()
        st.metric("Tổng Doanh thu", f"{total_revenue:,.0f} VNĐ")
    
    with col2:
        total_quantity = filtered_df['so luong'].sum()
        st.metric("Tổng Số lượng", f"{total_quantity:,.0f} lượt")
    
    with col3:
        avg_revenue = total_revenue / total_quantity if total_quantity > 0 else 0
        st.metric("Doanh thu TB/lượt", f"{avg_revenue:,.0f} VNĐ")
    
    with col4:
        num_sources = filtered_df['noi gioi thieu'].nunique()
        st.metric("Số nguồn giới thiệu", f"{num_sources} nguồn")
    
    # Create charts
    fig1, fig2, fig3, fig4, fig5, fig6 = create_charts(
        df, doanh_thu_theo_nguon, doanh_thu_theo_thang, 
        hieu_suat_nguon, pivot_doanh_thu, selected_sources, selected_months
    )
    
    # Display charts
    st.markdown("## 📊 Biểu đồ phân tích")
    
    # Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2
    st.plotly_chart(fig3, use_container_width=True)
    
    # Row 3
    st.plotly_chart(fig4, use_container_width=True)
    
    # Row 4
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig5, use_container_width=True)
    with col2:
        st.plotly_chart(fig6, use_container_width=True)
    
    # Data tables
    st.markdown("## 📋 Bảng dữ liệu chi tiết")
    
    tab1, tab2, tab3 = st.tabs(["Theo Nguồn", "Theo Tháng", "Hiệu suất"])
    
    with tab1:
        st.dataframe(
            doanh_thu_theo_nguon.style.format({
                'doanh thu': '{:,.0f}',
                'so luong': '{:,.0f}'
            }),
            use_container_width=True
        )
    
    with tab2:
        st.dataframe(
            doanh_thu_theo_thang.style.format({
                'doanh thu': '{:,.0f}',
                'so luong': '{:,.0f}'
            }),
            use_container_width=True
        )
    
    with tab3:
        st.dataframe(
            hieu_suat_nguon.style.format({
                'doanh thu': '{:,.0f}',
                'so luong': '{:,.0f}',
                'trung binh': '{:,.0f}'
            }),
            use_container_width=True
        )
    
    # Summary
    st.markdown("## 📝 Tóm tắt phân tích")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Top 3 Nguồn Giới thiệu")
        for i, (nguon, data) in enumerate(doanh_thu_theo_nguon.head(3).iterrows(), 1):
            percentage = data['doanh thu']/df['doanh thu'].sum()*100
            st.markdown(f"""
            **{i}. {nguon}**
            - Doanh thu: {data['doanh thu']:,.0f} VNĐ ({percentage:.1f}%)
            - Số lượng: {data['so luong']:,.0f} lượt
            """)
    
    with col2:
        st.markdown("### Thông tin thời gian")
        st.markdown(f"""
        - **Thời gian phân tích:** {df['thang'].min()} - {df['thang'].max()}
        - **Tổng số tháng:** {df['thang'].nunique()} tháng
        - **Tổng số nguồn:** {df['noi gioi thieu'].nunique()} nguồn
        """)

if __name__ == "__main__":
    main()