import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np

def update(grid):
    # 在网格周围填充一圈0（处理边界条件）
    padded_grid = np.pad(grid, pad_width=1, mode='constant')
    # 然后边界的细胞始终是死的（0），并且算邻居的时候也不算边界的细胞
    # 计算8个相邻方向的切片
    top         = padded_grid[:-2, 1:-1]  # 上
    bottom      = padded_grid[2:, 1:-1]   # 下
    left        = padded_grid[1:-1, :-2]  # 左
    right       = padded_grid[1:-1, 2:]   # 右
    top_left    = padded_grid[:-2, :-2]   # 左上
    top_right   = padded_grid[:-2, 2:]    # 右上
    bottom_left = padded_grid[2:, :-2]    # 左下
    bottom_right= padded_grid[2:, 2:]     # 右下
    
    # 计算每个细胞的存活邻居总数
    neighbors = top + bottom + left + right + top_left + top_right + bottom_left + bottom_right
    
    # 应用生存规则
    survive = (grid == 1) & ((neighbors == 2) | (neighbors == 3))  # 存活条件
    born = (grid == 0) & (neighbors == 3)                          # 新生条件
    
    # 生成新网格
    new_grid = np.where(survive | born, 1, 0)
    return new_grid

def init_grid(size=100):
    grid = np.zeros((size, size), dtype=int)
    # 画出刻度
    #ax.set_xticks(np.arange(0, size, 1))  # 每1格一个刻度
    #ax.set_yticks(np.arange(0, size, 1))
    # 添加滑翔机（Glider)
    #glider = np.array([
    #   [0, 1, 0],
    #   [0, 0, 1],
    #   [1, 1, 1]
    #])
    #grid[10:13, 10:13] = glider  # 在坐标 (10,10) 处放置滑翔机

    return grid

# 预定义图形库（坐标以图形左上角为原点 (0,0)）
PATTERNS = {
    # 静物
    'block': [(0,0), (0,1), (1,0), (1,1)],
    'beehive': [(0,1), (0,2), (1,0), (1,3), (2,1), (2,2)],
    
    # 振荡器
    'blinker': [(0,0), (1,0), (2,0)],
    'toad': [(1,0), (1,1), (1,2), (2,1), (2,2), (2,3)],
    'pulsar' : [
    (2,0), (3,0), (4,0),
    (0,2), (0,3), (0,4),
    (5,2), (5,3), (5,4),
    (2,5), (3,5), (4,5),
    # 对称部分
    (0,7), (0,8), (0,9),
    (2,7), (3,7), (4,7),
    (5,7), (5,8), (5,9),
    (2,10), (3,10), (4,10)
],
    # 太空船
    'glider': [(0,1), (1,2), (2,0), (2,1), (2,2)],
    'lwss': [(0,1), (0,2), (1,0), (2,0), (2,2), (3,0), (3,1), (3,2)],
    
    # 扩展图形
    'gosper_gun':
    [
        (5, 1), (5, 2), (6, 1), (6, 2),  # 左方方块
        (5, 11), (6, 11), (7, 11),       # 左方竖线
        (4, 12), (8, 12),                # 左方竖线两侧
        (3, 13), (9, 13),                # 左方竖线两侧
        (3, 14), (9, 14),                # 左方竖线两侧
        (6, 15),                         # 左方竖线中间
        (4, 16), (8, 16),                # 左方竖线两侧
        (5, 17), (6, 17), (7, 17),       # 左方竖线
        (6, 18),                         # 左方竖线中间
        (3, 21), (4, 21), (5, 21),       # 中间方块左侧
        (3, 22), (4, 22), (5, 22),       # 中间方块右侧
        (2, 23), (6, 23),                # 中间方块两侧
        (1, 25), (2, 25), (6, 25), (7, 25),  # 中间方块两侧
        (3, 35), (4, 35), (3, 36), (4, 36)   # 右方方块
    ],

    
}

def insert_pattern(grid, pattern_name, position):
    """
    在指定位置插入图形（先清理该区域）
    
    参数:
        grid (numpy.ndarray): 生命游戏网格
        pattern_name (str): 预定义图形名称
        position (tuple): 插入位置的左上角坐标 (x,y)
    
    返回:
        numpy.ndarray: 修改后的网格
    
    异常:
        ValueError: 图形不存在或越界
    """
    # 检查图形是否存在
    if pattern_name not in PATTERNS:
        raise ValueError(f"未知图形 '{pattern_name}'，可选图形：{list(PATTERNS.keys())}")
    
    # 获取图形坐标
    pattern = PATTERNS[pattern_name]
    
    # 计算图形覆盖区域尺寸
    max_x = max(dx for dx, dy in pattern)
    max_y = max(dy for dx, dy in pattern)
    width = max_x + 1
    height = max_y + 1
    
    # 解析插入位置
    x0, y0 = position
    x1 = x0 + max_x
    y1 = y0 + max_y
    
    # 检查边界
    grid_h, grid_w = grid.shape
    if x0 < 0 or y0 < 0 or x1 >= grid_h or y1 >= grid_w:
        raise ValueError(f"插入区域 [{x0}:{x1}, {y0}:{y1}] 超出网格范围 {grid.shape}")
    
    # 清理目标区域
    grid[x0:x1+1, y0:y1+1] = 0
    
    # 插入图形
    for dx, dy in pattern:
        x = x0 + dx
        y = y0 + dy
        grid[x, y] = 1
    
    return grid


# 创建一个初始网格
grid = init_grid(size=500)
fig, ax = plt.subplots()
ax.axis('off') # 关闭坐标轴


# 添加预定义图形
grid = insert_pattern(grid, 'gosper_gun', (0,0))
grid = insert_pattern(grid, 'gosper_gun', (0, 40))
grid = insert_pattern(grid, 'gosper_gun', (0, 80))
grid = insert_pattern(grid, 'gosper_gun', (0, 120))
grid = insert_pattern(grid, 'gosper_gun', (0, 160))
grid = insert_pattern(grid, 'gosper_gun', (0, 200))

grid = insert_pattern(grid, 'blinker', (140,154))
grid = insert_pattern(grid, 'blinker', (140,194))
grid = insert_pattern(grid, 'blinker', (140,234))
grid = insert_pattern(grid, 'blinker', (140,274))
grid = insert_pattern(grid, 'blinker', (140,314))
grid = insert_pattern(grid, 'blinker', (140,354))
grid = insert_pattern(grid, 'blinker', (140,394))

img = ax.imshow(grid, cmap='binary', interpolation='nearest', animated=True)

def animate(frame):
    global grid
    grid = update(grid)  # 更新网格
    img.set_array(grid)  # 更新图像数据
    return img,

ani = FuncAnimation(fig, animate, frames=100, interval=1, blit=True)
# ani.save('./pics/meet_toad.gif', writer='pillow',fps=20)
plt.show()
