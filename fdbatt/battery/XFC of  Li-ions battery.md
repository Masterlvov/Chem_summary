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

