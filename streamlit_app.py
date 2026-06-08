import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    import numpy as np
    import matplotlib.pyplot as plt
    import streamlit as st
    import pandas as pd


    st.set_page_config(page_title='단위원과 사인함수', layout='wide')

    ANGLE_OPTIONS = ['0', 'π/2', 'π', '3π/2', '2π']
    ANGLE_MAP = {
        '0': 0.0,
        'π/2': np.pi / 2,
        'π': np.pi,
        '3π/2': 3 * np.pi / 2,
        '2π': 2 * np.pi,
    }


    def plot_unit_circle(ax, angle_rad):
        # Base circle
        theta = np.linspace(0, 2 * np.pi, 400)
        x = np.cos(theta)
        y = np.sin(theta)
        ax.plot(x, y, color='k', linewidth=1)

        # Axes
        ax.axhline(0, color='k', linewidth=1)
        ax.axvline(0, color='k', linewidth=1)

        # Limits and aspect
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal', adjustable='box')

        # Grid and ticks
        ax.grid(True, linestyle='--', linewidth=0.5)
        ax.set_xticks(np.linspace(-1, 1, 5))
        ax.set_yticks(np.linspace(-1, 1, 5))

        # Selected point
        x_p = np.cos(angle_rad)
        y_p = np.sin(angle_rad)

        eps = 1e-9
        if abs(angle_rad) < eps:
            ax.plot(1.0, 0.0, marker='o', color='red', markersize=8)
        else:
            theta_red = np.linspace(0, angle_rad, max(2, int(200 * angle_rad / (2 * np.pi))))
            x_red = np.cos(theta_red)
            y_red = np.sin(theta_red)
            ax.plot(x_red, y_red, color='red', linewidth=3)
            ax.plot(x_p, y_p, marker='o', color='red', markersize=8)

        # Dashed projection lines to axes
        ax.plot([x_p, x_p], [0, y_p], color='gray', linestyle='--', linewidth=1)
        ax.plot([0, x_p], [y_p, y_p], color='gray', linestyle='--', linewidth=1)

        # θ label near the small arc
        mid_theta = angle_rad / 2 if angle_rad > 0 else 0.1
        label_r = 0.28
        ax.text(label_r * np.cos(mid_theta), label_r * np.sin(mid_theta), 'θ', color='black', fontsize=14)

        # Coordinate label
        coord_text = f'({x_p:.3f}, {y_p:.3f})'
        ax.text(x_p + 0.05 * np.sign(x_p if abs(x_p) > 1e-6 else 1), y_p + 0.05, coord_text, color='black')


    def plot_sine(ax, angle_rad):
        x = np.linspace(0, 2 * np.pi, 600)
        y = np.sin(x)
        ax.plot(x, y, color='k', linewidth=1)

        # Axes
        ax.axhline(0, color='k', linewidth=1)
        ax.axvline(0, color='k', linewidth=1)

        # Limits and ticks
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(-1.2, 1.2)
        xticks = [0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]
        xtick_labels = ['0', 'π/2', 'π', '3π/2', '2π']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels)
        ax.set_yticks([-1, 0, 1])
        ax.grid(True, linestyle='--', linewidth=0.5)

        # Highlight part and point
        eps = 1e-9
        if abs(angle_rad) < eps:
            ax.plot(0.0, 0.0, marker='o', color='red', markersize=8)
        else:
            mask = x <= angle_rad + 1e-12
            x_red = x[mask]
            y_red = y[mask]
            ax.plot(x_red, y_red, color='red', linewidth=3)
            ax.plot(angle_rad, np.sin(angle_rad), marker='o', color='red', markersize=8)

        # Dashed projection lines: vertical to x-axis and horizontal to y-axis
        ax.plot([angle_rad, angle_rad], [0, np.sin(angle_rad)], color='gray', linestyle='--', linewidth=1)
        ax.plot([0, angle_rad], [np.sin(angle_rad), np.sin(angle_rad)], color='gray', linestyle='--', linewidth=1)


    def main():
        st.title('단위원과 사인함수')

        sel = st.selectbox('각도를 선택하세요', ANGLE_OPTIONS, index=0)
        angle = ANGLE_MAP[sel]

        col1, col2 = st.columns([1, 1])

        # Left: unit circle
        with col1:
            fig1, ax1 = plt.subplots(figsize=(4, 4))
            plot_unit_circle(ax1, angle)
            st.pyplot(fig1)

        # Right: sine
        with col2:
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            plot_sine(ax2, angle)
            st.pyplot(fig2)

        # Values table under the plots
        sin_val = np.sin(angle)
        cos_val = np.cos(angle)
        radians = angle

        df = pd.DataFrame({
            '항목': ['각도', '라디안', 'sin', 'cos'],
            '값': [sel, f'{radians:.6f}', f'{sin_val:.6f}', f'{cos_val:.6f}']
        })

        st.markdown('**선택된 값**')
        st.table(df)


    if __name__ == '__main__':
        main()
