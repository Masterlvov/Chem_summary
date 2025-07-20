# 快充的实现
## 瓶颈问题
### 多孔电极快充存在的问题
 快充下大电流密度下，锂离子由于扩散层的快速增长，导致底层锂离子快速反应完之后锂离子无法扩散到电极深处，导致锂离子扩散至可到达区域（表层石墨）的活性物质嵌锂饱和后（嵌锂过电势高于析锂过电势），石墨表面发生析锂；而底层石墨双电层快速充电，电势降低。使得负极表面SOC高，电位低，在石墨表面析锂。

 那么如何让锂离子能够更好的扩散进电极深处，根据菲克扩散定律，我们可以知道，扩散通量取决于浓度差以及时间（或者特征长度即扩散距离（特征时间$\tau $ = $L^2/D$））特征尺度L，扩散系数D，特征时间$\tau$。那么要么相同时间内浓度差足够大，要么特征长度即扩散距离很短。

 扩散距离其实由于电极设计参数比如面密度、压实使得很难改变（但可以设计相同压实下的不同孔隙结构实现），但一开始的浓度差是可以通过劣化表层并优化底层的反应能力来实现的。但是表层的能力又不能太差，防止表层能力太差而析锂。

 文献里以及早期实验都明确了电极设计需要上大下小孔隙结构，这个是可以认为是改变锂离子有效扩散距离，也就是特征时间。

### 平板电极存在的问题（锂金属电池）
 sand‘s time 模型
 浓差极化-尖端效应？


 ## 解决办法
### 多孔电极下的提升
- 石墨出发调整
  - 石墨材料

### 平板电极下的提升


## XFC Problem of Material level
### 限制问题
refer from----Kinetic Limits of Graphite Anode for Fast-Charging Lithium-Ion Batteries
[doi](https://doi.org/10.1007/s40820-023-01183-6)
[url](https://link.springer.com/article/10.1007/s40820-023-01183-6#article-info)\
The rapid voltage change is attributed to the Li+ diffusion in the electrolyte and the short-range interface, while the subsequent slow change is ascribed to the Li+ diffusion through the long-range particle and electrode 电压的快速变化归因于 Li+ 在电解质和短程界面中的扩散，而随后的缓慢变化则归因于 Li+ 在长程粒子和电极中的扩散。\
The slight rise of Li+ diffusion coefficient is probably owing to the increased defective structures and strains in the graphite facilitating the Li+ diffusion. Based on the lowest Li+ diffusion coefficient ($2.64 × 10^−10 cm^2 s^−1$), the time for Li+ diffusing from the surface to the bulk center of graphite with a diameter of 10 μm is estimated to be about 7.89 min .( $\tau =L^2/2D$)   

$\ln \left[ {\exp \left( {\frac{{\varphi_{\infty } - \varphi }}{RT}F} \right) - 1} \right] = - \frac{{\pi^{2} }}{{L^{2} }}Dt - \ln N$ \
whereF is the Faraday constant, R is the molar gas constant, T is the thermodynamic temperature, and L is the thickness of the electrode $N = \frac{{\exp \left( { - \frac{{\pi^{2} }}{{L^{2} }}D\xi } \right)}}{{\exp \left( {\frac{{\varphi_{\infty } - \varphi_{\xi } }}{RT}F} \right) - 1}}$
 when t = ξ, the voltage is ${{\varphi }}_{{\upxi }}$, which can be measured experimentally.
The time for Li+ diffusing from the surface to the bulk center of graphite with a diameter of d (tdiffusion) is estimated by Eq. $t_{{{\text{diffusion}}}} = \frac{{(d/2)^{2} }}{{2D_{\min } }}$

how this equation derivated ?
### 在实际体系中测量的难点
[石墨负极表面浓度饱和析锂模型](https://ars.els-cdn.com/content/image/1-s2.0-S254243512030619X-gr5.jpg)
 析锂是否会发生是热力学和动力学综合作用的结果，仅仅考虑负极表面电位是否低于 0mV 是不严谨的。当石墨表面电位(相对于 Li/Li+) 低于 0mV 时，析锂在热力学上是有可能发生的，但是实验发现石墨极表面析锂之前的电位可以达到 -200到 -400mV [1]。为了解释这些实验现象，Bazant et al.提出了一种负极表面浓度饱和析锂模型，即当锂离子在负极表面嵌满时，嵌锂反应会很难继续发生，，施加的电流密度会被用于析锂反应 [2]。负极的表面浓度达到饱和的原因是锂离子的固相扩散速率远小于电图1展示了饱和析锂模型，1(A)表示嵌锂反应和析锂反应的竞争，1(B)展示了石墨在嵌锂不同阶段的相变，1(C)展示了嵌锂过程中锂离子化学势的变化，化学势与石墨表面电位的关系如下\[
V = -\frac{\mu_{Li}}{e} + \eta_{pl} = -\frac{\mu_s}{e} + \eta_{int}
\] ，其中  是嵌入态锂离 是嵌锂反应的过电势（符号为负）。在1-2阶段,  (即)，析锂在热力学上不可能发生，其中 是锂金属的化学势，以锂金属为参照物时可以认为是0。随着锂离子的不断嵌入， 不断增大， 变得越来石墨的表面电位 V不断减小，在3-4阶段满足，此时析锂在热力学上可能发生。但是由于 , 从能量的角度嵌锂更倾向于发生。从动力学的角度看，嵌锂反应不需要克服析锂反应所需的成核势垒 (Nucleation barrier)，也更容易发生。这解释了为什么在表面电位刚刚小于0 mV时，析锂反应没有立刻发生。当表面浓度达到饱和时（图1D阶段5可以看到 ，从能量角度看嵌锂反应和析锂反应有同等可能发生。从动力学角度看，嵌锂反应很难发生，因为表面没有可以可嵌入的空间。相反，析锂反应动力学上容易发生，因为 LiC6的形成降低了成核势垒 [3]。析锂一旦发生，随后过程中锂枝晶生长所需克服的能垒会大幅减少（图1D阶段6），之后的反应由析锂占主导。总结来说，当负极表面电位小于 0mV 时，析锂反应虽然在热力学上可能发生，但是只有当表面浓度达到饱和时，析锂在动力学上才更倾向于发生。上述的浓度饱和析锂模型很难在实验用来当作快充边界，因为实验方法难以实时监测固相锂离子浓度。基于P2D 模型的电化学仿真可以实时监测固相锂离子浓度，以负极表面浓度饱和为边界，可以使用算法来寻找快充策略，研究化学体系的极限快充能力。同时电化学仿真可以分析电流密度分布、电解液浓度分布、不同颗粒之间 SOC 分布，帮助实验理解局部析锂的原因。\\
ref from --- Interplay of Lithium Intercalation and Plating on a Single Graphite Particle 
[doi](https://doi.org/10.1016/j.joule.2020.12.020)\\
 制定快充策略时的一个重要考虑因素是快充边界。虽然以析锂为快充边界可以在理论上找到化学体系的快充极限，但是在实验过程中难以实时检测是否析锂。用三电极监测负极表面电位，以 0mV为析锂边界，三电极法忽略了从隔膜到负极表面的电解液欧姆电压降以及负极集流体到隔膜处的电子欧姆电压降，这意味着三电极读数为 0mV 时，负极表面实际电位高于 0mV，由此所得到的策略会低估体系的快充能力。\\
 
