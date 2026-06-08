import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


st.set_page_config(page_title="단위원과 사인 함수 시각화", layout="wide")

ANGLE_OPTIONS = ["0", "π/2", "π", "3π/2", "2π"]
ANGLE_MAP = {
    "0": 0.0,
    "π/2": np.pi / 2,
    "π": np.pi,
    "3π/2": 3 * np.pi / 2,
    "2π": 2 * np.pi,
}


def plot_unit_circle(angle_rad):
    fig, ax = plt.subplots(figsize=(4, 4))
    # Base circle
    theta = np.linspace(0, 2 * np.pi, 400)
    x = np.cos(theta)
    y = np.sin(theta)
    ax.plot(x, y, color="k", linewidth=1)

    # Axes through origin
    ax.axhline(0, color="k", linewidth=1)
    ax.axvline(0, color="k", linewidth=1)

    # Limits and aspect
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal', adjustable='box')

    # Grid and ticks
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_xticks(np.linspace(-1, 1, 5))
    ax.set_yticks(np.linspace(-1, 1, 5))

    # Highlighted red part
    eps = 1e-9
    if abs(angle_rad) < eps:
        # Only a red point at (1,0)
        ax.plot(1.0, 0.0, marker='o', color='red', markersize=8)
    else:
        theta_red = np.linspace(0, angle_rad, max(2, int(200 * angle_rad / (2 * np.pi))))
        x_red = np.cos(theta_red)
        y_red = np.sin(theta_red)
        ax.plot(x_red, y_red, color='red', linewidth=3)
        # endpoint
        ax.plot(np.cos(angle_rad), np.sin(angle_rad), marker='o', color='red', markersize=8)

    fig.tight_layout()
    return fig


def plot_sine(angle_rad):
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 2 * np.pi, 600)
    y = np.sin(x)
    # base sine
    ax.plot(x, y, color='k', linewidth=1)

    # Axes
    ax.axhline(0, color='k', linewidth=1)
    ax.axvline(0, color='k', linewidth=1)

    # Limits
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1.2, 1.2)

    # Ticks
    xticks = [0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]
    xtick_labels = ["0", "π/2", "π", "3π/2", "2π"]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)
    ax.set_yticks([-1, 0, 1])

    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    eps = 1e-9
    if abs(angle_rad) < eps:
        # Only a red point at (0,0)
        ax.plot(0.0, 0.0, marker='o', color='red', markersize=8)
    else:
        mask = x <= angle_rad + 1e-12
        x_red = x[mask]
        y_red = y[mask]
        ax.plot(x_red, y_red, color='red', linewidth=3)
        ax.plot(angle_rad, np.sin(angle_rad), marker='o', color='red', markersize=8)

    fig.tight_layout()
    return fig


def main():
    st.title("단위원과 사인 함수 시각화")

    sel = st.selectbox("각도를 선택하세요", ANGLE_OPTIONS, index=0)
    angle = ANGLE_MAP[sel]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.pyplot(plot_unit_circle(angle))

    with col2:
        st.pyplot(plot_sine(angle))


if __name__ == '__main__':
    main()
