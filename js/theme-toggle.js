/**
 * Theme Toggle System - iOS 26 Liquid Glass
 * 管理深色/浅色主题切换
 */

(function() {
    'use strict';

    const THEME_KEY = 'mambo-theme';
    const THEME_DARK = 'dark';
    const THEME_LIGHT = 'light';

    class ThemeManager {
        constructor() {
            this.currentTheme = this.getSavedTheme() || THEME_DARK; // 默认深色
            this.toggleBtn = null;
            this.lightIcon = null;
            this.darkIcon = null;
        }

        /**
         * 初始化主题系统
         */
        init() {
            // 获取DOM元素
            this.toggleBtn = document.getElementById('themeToggle');
            this.lightIcon = document.getElementById('themeIconLight');
            this.darkIcon = document.getElementById('themeIconDark');

            if (!this.toggleBtn || !this.lightIcon || !this.darkIcon) {
                console.warn('Theme toggle elements not found');
                return;
            }

            // 应用保存的主题
            this.applyTheme(this.currentTheme, false);

            // 绑定点击事件
            this.toggleBtn.addEventListener('click', () => this.toggleTheme());

            console.log('✅ Theme Manager initialized:', this.currentTheme);
        }

        /**
         * 从 localStorage 获取保存的主题
         */
        getSavedTheme() {
            try {
                return localStorage.getItem(THEME_KEY);
            } catch (e) {
                console.warn('LocalStorage not available:', e);
                return null;
            }
        }

        /**
         * 保存主题到 localStorage
         */
        saveTheme(theme) {
            try {
                localStorage.setItem(THEME_KEY, theme);
            } catch (e) {
                console.warn('Could not save theme:', e);
            }
        }

        /**
         * 应用主题
         * @param {string} theme - 'dark' 或 'light'
         * @param {boolean} animate - 是否动画过渡
         */
        applyTheme(theme, animate = true) {
            const html = document.documentElement;

            // 如果需要动画，添加过渡类
            if (animate) {
                html.style.transition = 'background-color 0.3s ease, color 0.3s ease';
                setTimeout(() => {
                    html.style.transition = '';
                }, 300);
            }

            // 设置 data-theme 属性
            html.setAttribute('data-theme', theme);
            this.currentTheme = theme;

            // 更新图标显示
            if (theme === THEME_DARK) {
                this.lightIcon.classList.remove('hidden');
                this.darkIcon.classList.add('hidden');
            } else {
                this.lightIcon.classList.add('hidden');
                this.darkIcon.classList.remove('hidden');
            }

            // 更新按钮 aria-label
            const label = theme === THEME_DARK ? 'Switch to light mode' : 'Switch to dark mode';
            this.toggleBtn.setAttribute('aria-label', label);

            // 保存到 localStorage
            this.saveTheme(theme);

            // 触发自定义事件，供其他模块监听
            const event = new CustomEvent('themechange', {
                detail: { theme }
            });
            document.dispatchEvent(event);

            console.log('🎨 Theme applied:', theme);
        }

        /**
         * 切换主题
         */
        toggleTheme() {
            const newTheme = this.currentTheme === THEME_DARK ? THEME_LIGHT : THEME_DARK;
            this.applyTheme(newTheme, true);

            // 添加轻微的触觉反馈效果（如果浏览器支持）
            if ('vibrate' in navigator) {
                navigator.vibrate(10);
            }
        }

        /**
         * 获取当前主题
         */
        getCurrentTheme() {
            return this.currentTheme;
        }

        /**
         * 检查是否为深色模式
         */
        isDarkMode() {
            return this.currentTheme === THEME_DARK;
        }
    }

    // 创建全局实例
    window.themeManager = new ThemeManager();

    // DOM 加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.themeManager.init();
        });
    } else {
        window.themeManager.init();
    }

    // 监听主题变化事件（供调试）
    document.addEventListener('themechange', (e) => {
        console.log('📢 Theme changed to:', e.detail.theme);
    });

})();
