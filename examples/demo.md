# 中文 LaTeX 渲染示例

## 1. 行内与块级公式

爱因斯坦质能方程 $E = mc^2$，其中 $c$ 为光速。也支持 \(\alpha + \beta = \gamma\) 写法。

高斯积分：

$$
\int_{-\infty}^{+\infty} e^{-x^2}\,\mathrm{d}x = \sqrt{\pi}
$$

## 2. 公式中的中文

$$
\text{速度} = \frac{\text{位移}}{\text{时间}}, \qquad v = \frac{\Delta x}{\Delta t}
$$

\[
f(x) = \begin{cases} x^2, & \text{当 } x \ge 0 \\ -x, & \text{当 } x < 0 \end{cases}
\]

## 3. 多行对齐（amsmath）

\begin{align}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \times \mathbf{B} &= \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\end{align}

## 4. 矩阵、化学式、物理宏包

$$
A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}, \quad \det A = -2
$$

水的电解：$\ce{2H2O -> 2H2 ^ + O2 ^}$，薛定谔方程 $i\hbar \pdv{t}\ket{\psi} = \hat{H}\ket{\psi}$。

## 5. Markdown 混排

| 名称 | 公式 |
|------|------|
| 欧拉公式 | $e^{i\pi} + 1 = 0$ |
| 勾股定理 | $a^2 + b^2 = c^2$ |

代码中的 `$x_1$` 不会被渲染。下划线 $a_1 * b_2 * c_3$ 不会被 Markdown 误当成斜体。
