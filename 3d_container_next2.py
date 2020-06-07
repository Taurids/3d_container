from vtk import *
import vtk
import functools
import random
import math

# 数据生成，输入为箱子种类数，箱子最大长、最小长、最大宽、最小宽、商品个数、商品最大长、最小长、最大宽、最小宽
# 输出为生成的箱子列表和商品列表
def boxs_generate_3d(nums_box=20, max_l_box=80, min_l_box=21, max_w_box=60, min_w_box=14, max_h_box=60, min_h_box=9):

    # 随机生成箱子
    boxs = []
    for i in range(nums_box):
        boxs.append([int((max_l_box-min_l_box) * random.random() + min_l_box),
                     int((max_w_box-min_w_box) * random.random() + min_w_box),
                     int((max_h_box-min_h_box) * random.random() + min_h_box)])
    # boxs = []
    # for i in range(nums_box):
    #     boxs.append([int((max_l_box-min_l_box) * random.random() + min_l_box),
    #                  int((max_w_box-min_w_box) * random.random() + min_w_box),
    #                  int((max_h_box-min_h_box) * random.random() + min_h_box)])
    return boxs

# 二维商品排序用
def cmp_2d(x,y):
    if x[0] < y[0]:
        return -1
    elif x[0] > y[0]:
        return 1
    elif x[1] < y[1]:
        return -1
    elif x[1] > y[1]:
        return 1
    else:
        return 0


# 三维商品排序用
def cmp_3d(x, y):
    if x[0] < y[0]:
        return -1
    elif x[0] > y[0]:
        return 1
    elif x[1] < y[1]:
        return -1
    elif x[1] > y[1]:
        return 1
    elif x[2] < y[2]:
        return -1
    elif x[2] > y[2]:
        return 1
    else:
        return 0


# 检验是否每个商品都能有一个箱子放下它
def check_3d(boxs, goods):
    for good in goods:
        can_put = False
        for box in boxs:
            if good[0] <= box[0] and good[1] <= box[1] and good[2] <= box[2]:
                can_put = True
                break
        if not can_put:
            print(good,"太大，无合适箱子")
            return False
    return True


def can_put_3d(l, w, h, goods):
    L = max(l, w, h)
    H = min(l, w, h)
    W = l + w + h - L - H

    for good in goods:
        # lg, wg, hg = good[0], good[1], good[2]
        lg = max(good[0], good[1], good[2])
        hg = min(good[0], good[1], good[2])
        wg = good[0] + good[1] + good[2] - lg - hg
        if lg > L or wg > W or hg > H:
            return False
    return True

# 先以w为限制码垛，再以l为限制码垛
# 输入为长、宽、商品集，输出为箱子个数
def packing_simple(l, w, h, goods):

    # 先检查是否每一个商品在此规则下都能放下
    if not can_put_3d(l, w, h, goods):
        return -1

    #以h为限制码垛成条，商品排序，大的放前面
    goods1 = []
    for good in goods:
        if good[0] <= l and good[1] <= w and good[2] <= h:
            goods1.append([good[0], good[1], good[2]])
        elif good[0] <= l and good[2] <= w and good[1] <= h:
            goods1.append([good[0], good[2], good[1]])
        elif good[1] <= l and good[0] <= w and good[2] <= h:
            goods1.append([good[1], good[0], good[2]])
        elif good[1] <= l and good[2] <= w and good[0] <= h:
            goods1.append([good[1], good[2], good[0]])
        elif good[2] <= l and good[0] <= w and good[1] <= h:
            goods1.append([good[2], good[0], good[1]])
        else:
            goods1.append([good[2], good[1], good[0]])

    goods1 = sorted(goods1, key=functools.cmp_to_key(cmp_3d), reverse=True)

    strips = []
    goods1_used = [0 for i in range(len(goods1))]

    while sum(goods1_used) < len(goods1_used):
        l_used = 0
        w_used = 0
        h_used = 0
        for i in range(len(goods1_used)):
            if goods1_used[i] == 0 and h_used + goods1[i][2] <= h:
                l_used = max(l_used, goods1[i][0])
                w_used = max(w_used, goods1[i][1])
                h_used += goods1[i][2]
                goods1_used[i] = 1
        strips.append([l_used, w_used])

    strips = sorted(strips, key=functools.cmp_to_key(cmp_2d), reverse=True)

    #以w为限制码垛成层
    levels = []
    strip_used = [0 for i in range(len(strips))]

    while sum(strip_used) < len(strip_used):
        l_used = 0
        w_used = 0
        for i in range(len(strips)):
            if strip_used[i] == 0 and w_used + strips[i][1] <= w:
                l_used = max(l_used, strips[i][0])
                w_used += strips[i][1]
                strip_used[i] = 1
        levels.append(l_used)

    #再以l为限制码垛
    levels = sorted(levels, reverse=True)
    L_box_unused = [l]

    for level in levels:
        flag = -1
        for i in range(len(L_box_unused)):
            if L_box_unused[i] >= level:
                if flag == -1:
                    flag = i
                elif L_box_unused[i] < L_box_unused[flag]:
                    flag = i
        if flag == -1:
            L_box_unused.append(l - level)
        else:
            L_box_unused[flag] -= level

    return len(L_box_unused)


# 选择合适的主箱子
def box_choose_3d(boxs, nums_simplePacking_1, nums_simplePacking_2, nums_simplePacking_3, nums_simplePacking_4, nums_simplePacking_5, nums_simplePacking_6):
    l = -1
    w = -1
    h = -1
    nums = -1
    for i in range(len(boxs)):
        if nums_simplePacking_1[i] != -1:
            if nums == -1 or (nums != -1 and nums > nums_simplePacking_1[i]) or (nums != -1 and nums == nums_simplePacking_1[i] and l * w * h > boxs[i][0] * boxs[i][1] * boxs[i][2]):
                l = boxs[i][0]
                w = boxs[i][1]
                h = boxs[i][2]
                nums = nums_simplePacking_1[i]
        if nums_simplePacking_2[i] != -1:
            if nums == -1 or (nums != -1 and nums > nums_simplePacking_2[i]) or (nums != -1 and nums == nums_simplePacking_2[i] and l * w * h > boxs[i][0] * boxs[i][1] * boxs[i][2]):
                l = boxs[i][0]
                w = boxs[i][2]
                h = boxs[i][1]
                nums = nums_simplePacking_2[i]
        if nums_simplePacking_3[i] != -1:
            if nums == -1 or (nums != -1 and nums > nums_simplePacking_3[i]) or (nums != -1 and nums == nums_simplePacking_3[i] and l * w * h > boxs[i][0] * boxs[i][1] * boxs[i][2]):
                l = boxs[i][1]
                w = boxs[i][0]
                h = boxs[i][2]
                nums = nums_simplePacking_3[i]
        if nums_simplePacking_4[i] != -1:
            if nums == -1 or (nums != -1 and nums > nums_simplePacking_4[i]) or (nums != -1 and nums == nums_simplePacking_4[i] and l * w * h > boxs[i][0] * boxs[i][1] * boxs[i][2]):
                l = boxs[i][1]
                w = boxs[i][2]
                h = boxs[i][0]
                nums = nums_simplePacking_4[i]
        if nums_simplePacking_5[i] != -1:
            if nums == -1 or (nums != -1 and nums > nums_simplePacking_5[i]) or (nums != -1 and nums == nums_simplePacking_5[i] and l * w * h > boxs[i][0] * boxs[i][1] * boxs[i][2]):
                l = boxs[i][2]
                w = boxs[i][0]
                h = boxs[i][1]
                nums = nums_simplePacking_5[i]
        if nums_simplePacking_6[i] != -1:
            if nums == -1 or (nums != -1 and nums > nums_simplePacking_6[i]) or (nums != -1 and nums == nums_simplePacking_6[i] and l * w * h > boxs[i][0] * boxs[i][1] * boxs[i][2]):
                l = boxs[i][2]
                w = boxs[i][1]
                h = boxs[i][0]
                nums = nums_simplePacking_6[i]
    return l, w, h


def packing_3d(l, w, h, goods):
    # 先检查是否每一个商品在此规则下都能放下
    if not can_put_3d(l, w, h, goods):
        return -1

    # 以h为限制码垛成条，商品排序，大的放前面
    goods1 = []
    for good in goods:
        if good[0] <= l and good[1] <= w and good[2] <= h:
            goods1.append([good[0], good[1], good[2]])
        elif good[0] <= l and good[2] <= w and good[1] <= h:
            goods1.append([good[0], good[2], good[1]])
        elif good[1] <= l and good[0] <= w and good[2] <= h:
            goods1.append([good[1], good[0], good[2]])
        elif good[1] <= l and good[2] <= w and good[0] <= h:
            goods1.append([good[1], good[2], good[0]])
        elif good[2] <= l and good[0] <= w and good[1] <= h:
            goods1.append([good[2], good[0], good[1]])
        else:
            goods1.append([good[2], good[1], good[0]])

    goods1 = sorted(goods1, key=functools.cmp_to_key(cmp_3d), reverse=True)

    strips = []
    strips_goods = []
    goods1_used = [0 for _ in range(len(goods1))]

    while sum(goods1_used) < len(goods1_used):
        l_used = 0
        w_used = 0
        h_used = 0
        strip_goods = []
        for i in range(len(goods1_used)):
            if goods1_used[i] == 0 and h_used + goods1[i][2] <= h:
                l_used = max(l_used, goods1[i][0])
                w_used = max(w_used, goods1[i][1])
                strip_goods.append([goods1[i][0], goods1[i][1], goods1[i][2], 0, 0, h_used])
                h_used += goods1[i][2]
                goods1_used[i] = 1
        strips.append([l_used, w_used])
        strips_goods.append(strip_goods)

        # 以w为限制码垛成层
    for i in range(len(strips)-1):
        for j in range(i+1, len(strips)):
            if strips[i][0] < strips[j][0] or (strips[i][0] == strips[j][0] and strips[i][1] < strips[j][1]):
                temp = strips[i]
                strips[i] = strips[j]
                strips[j] = temp
                temp1 = strips_goods[i]
                strips_goods[i] = strips_goods[j]
                strips_goods[j] = temp1

    levels = []
    levels_goods = []
    strip_used = [0 for _ in range(len(strips))]

    while sum(strip_used) < len(strip_used):
        l_used = 0
        w_used = 0
        level_goods = []
        for i in range(len(strips)):
            if strip_used[i] == 0 and w_used + strips[i][1] <= w:
                l_used = max(l_used, strips[i][0])
                for g in strips_goods[i]:
                    level_goods.append([g[0], g[1], g[2], 0, w_used, g[5]])
                w_used += strips[i][1]
                strip_used[i] = 1
        levels.append(l_used)
        levels_goods.append(level_goods)

    # 再以l为限制码垛
    for i in range(len(levels)-1):
        for j in range(i+1, len(levels)):
            if levels[i] < levels[j]:
                temp = levels[i]
                levels[i] = levels[j]
                levels[j] = temp
                temp1 = levels_goods[i]
                levels_goods[i] = levels_goods[j]
                levels_goods[j] = temp1

    L_box_unused = [l]
    L_goods = []
    L_coordinates = []

    L_goods.append([])
    L_coordinates.append([])
    num_select_list = []
    num_select = 20

    for i in range(len(levels)):
        flag = -1
        for j in range(len(L_box_unused)):
            if L_box_unused[j] >= levels[j] and num_select > 0:
                if flag == -1 or (flag != -1 and L_box_unused[j] < L_box_unused[flag]):
                    flag = j
        if flag == -1:
            L_box_unused.append(l - levels[i])
            L_goods.append([levels_goods[i][j][:3] for j in range(len(levels_goods[i]))])
            L_coordinates.append([levels_goods[i]])
            num_select = 20 - len(levels_goods[i])
        else:
            L_box_unused[flag] -= levels[i]
            num_select -= len(levels_goods[i])
            if num_select > 0:
                L_goods[flag] += [levels_goods[i][j][:3] for j in range(len(levels_goods[i]))]
                if len(L_coordinates[flag]) == 0:
                    L_coordinates[flag] += [levels_goods[i]]
                else:
                    L_coordinates[flag] += [[[levels_goods[i][j][0], levels_goods[i][j][1], levels_goods[i][j][2],
                                            L_coordinates[flag][-1][0][0] + L_coordinates[flag][-1][0][3],
                                            levels_goods[i][j][4], levels_goods[i][j][5]] for j in range(len(levels_goods[i]))]]
            else:
                L_box_unused.append(l - levels[i])
                L_goods.append([levels_goods[i][j][:3] for j in range(len(levels_goods[i]))])
                L_coordinates.append([levels_goods[i]])
                num_select = 20 - len(levels_goods[i])
        num_select_list.append(num_select)
        num_select_min = min(num_select_list)
    L_coordinates_merge = []

    for i in range(len(L_coordinates)):
        L_coordinates_i = []
        for j in range(len(L_coordinates[i])):
            L_coordinates_i += L_coordinates[i][j]
        L_coordinates_merge.append(L_coordinates_i)

    L_box = [[l, w, h] for i in range(len(L_box_unused))]

    return L_box, L_goods, L_coordinates_merge, num_select_min

# 正交二叉树启发式，试每一种箱子装下所有的商品需要的个数，取最少的，再去缩减最后一个箱子
def OBT_3d(boxs, goods):

    # 分别以长宽作为限制，依次码垛成层
    nums_simplePacking_1 = []
    nums_simplePacking_2 = []
    nums_simplePacking_3 = []
    nums_simplePacking_4 = []
    nums_simplePacking_5 = []
    nums_simplePacking_6 = []

    for box in boxs:
        nums_simplePacking_1.append(packing_simple(box[0], box[1], box[2], goods))
        nums_simplePacking_2.append(packing_simple(box[0], box[2], box[1], goods))
        nums_simplePacking_3.append(packing_simple(box[1], box[0], box[2], goods))
        nums_simplePacking_4.append(packing_simple(box[1], box[2], box[0], goods))
        nums_simplePacking_5.append(packing_simple(box[2], box[0], box[1], goods))
        nums_simplePacking_6.append(packing_simple(box[2], box[1], box[0], goods))

    # 找箱子数最少的箱子
    l, w, h = box_choose_3d(boxs, nums_simplePacking_1, nums_simplePacking_2, nums_simplePacking_3,
                            nums_simplePacking_4, nums_simplePacking_5, nums_simplePacking_6)
    print(l, w, h)
    # 装载
    L_box, L_goods, L_coordinates, num_select_min = packing_3d(l, w, h, goods)

    return L_box, L_goods, L_coordinates, num_select_min


# 检验结果中的商品集是否和原始的商品集一致
def goods_check(goods, L_goods):

    nums = 0
    for gs in L_goods:
        nums += len(gs)

    if len(goods) == nums:
        return True

    return False


# 添加商品图形
def Addcube_3d(ren, coordinate, edge_max, x_re, y_re, z_re):
    cube = vtk.vtkCubeSource()
    cube.SetXLength(coordinate[0]/edge_max)
    cube.SetYLength(coordinate[1]/edge_max)
    cube.SetZLength(coordinate[2]/edge_max)
    cube.Update()

    translation = vtk.vtkTransform()
    translation.Translate((coordinate[3] + coordinate[0]/2.0)/edge_max + x_re, (coordinate[4] + coordinate[1]/2.0)/edge_max + y_re, (coordinate[5] + coordinate[2]/2.0)/edge_max + z_re)
    transformFilter = vtkTransformPolyDataFilter()
    transformFilter.SetInputConnection(cube.GetOutputPort())
    transformFilter.SetTransform(translation)
    transformFilter.Update()

    transformedMapper = vtkPolyDataMapper()
    transformedMapper.SetInputConnection(transformFilter.GetOutputPort())
    transformedActor = vtkActor()
    transformedActor.SetMapper(transformedMapper)
    transformedActor.GetProperty().SetColor((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))

    ren.AddActor(transformedActor)


def png_save(renWin, name):
    windowToImageFilter = vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renWin)
    windowToImageFilter.Update()
    writer = vtkPNGWriter()
    writer.SetFileName(name)
    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    writer.Write()


# 三维展示，输入为箱子集和商品集，包裹的箱子和商品集一一对应
def show_3d(L_box, L_coordinates):

    nums = len(L_box)
    edge_max = max([max(L_box[i]) for i in range(len(L_box))]) if max([max(L_box[i]) for i in range(len(L_box))]) > 0 else 1

    # 预设参数
    gap = 0.01
    CL_p = 1.1
    CW_p = nums + gap * (nums - 1)
    CH_p = 0.01
    gap = 0.25

    x_re = 0
    y_re = 0
    z_re = 0

    #渲染及渲染窗口，并根据捕捉的鼠标事件执行相应的操作
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(1200, 600)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)


    """画容器"""
    for i in range(nums):

        cube = vtk.vtkCubeSource()
        cube.SetXLength(L_box[i][0]/edge_max)
        cube.SetYLength(L_box[i][1]/edge_max)
        cube.SetZLength(L_box[i][2]/edge_max)
        cube.Update()

        translation = vtkTransform()
        translation.Translate(L_box[i][0]/edge_max/2.0 + x_re, L_box[i][1]/edge_max/2.0 + i + gap*i + y_re, L_box[i][2]/edge_max/2.0 + z_re)
        transformFilter = vtkTransformPolyDataFilter()
        transformFilter.SetInputConnection(cube.GetOutputPort())
        transformFilter.SetTransform(translation)
        transformFilter.Update()

        transformedMapper = vtkPolyDataMapper()
        transformedMapper.SetInputConnection(transformFilter.GetOutputPort())
        transformedActor = vtkActor()
        transformedActor.SetMapper(transformedMapper)
        transformedActor.GetProperty().SetColor((1, 1, 1))
        transformedActor.GetProperty().SetRepresentationToWireframe()

        ren.AddActor(transformedActor)

    """画托盘"""
    cube = vtk.vtkCubeSource()
    cube.SetXLength(CL_p)
    cube.SetYLength(CW_p)
    cube.SetZLength(CH_p)
    cube.Update()

    translation = vtkTransform()
    translation.Translate(CL_p/2.0 + x_re, CW_p/2.0 + y_re, -CH_p/2.0 + z_re)
    transformFilter = vtkTransformPolyDataFilter()
    transformFilter.SetInputConnection(cube.GetOutputPort())
    transformFilter.SetTransform(translation)
    transformFilter.Update()

    transformedMapper = vtkPolyDataMapper()
    transformedMapper.SetInputConnection(transformFilter.GetOutputPort())
    transformedActor = vtkActor()
    transformedActor.SetMapper(transformedMapper)
    transformedActor.GetProperty().SetColor((0.2, 0.4, 0.8))

    ren.AddActor(transformedActor)

    for i in range(len(L_coordinates)):
        for j in range(len(L_coordinates[i])):
            Addcube_3d(ren, L_coordinates[i][j], edge_max, x_re, i + gap*i + y_re, z_re)

    camera = vtk.vtkCamera()
    camera.SetViewUp(0, 0, 1)  # 设置相机的“上”方向
    camera.SetPosition(10, 10, 1)  # 位置：世界坐标系，设置相机位置
    camera.SetFocalPoint(0, 8, 0)
    camera.ComputeViewPlaneNormal()
    # camera.SetPosition(5, -0.5, 2)
    ren.SetActiveCamera(camera)

    iren.Initialize()
    renWin.Render()
    # 保存过程
    png_save(renWin, "result_D3.png")
    # 展示
    iren.Start()


def exchange_item(items):  # 第一类邻域选择，随机交换两个物品
    s1, s2 = random.randint(0, len(items) - 1), random.randint(0, len(items) - 1)
    while s1 == s2:
        s2 = random.randint(0, len(goods) - 1)
    items[s1], items[s2], = items[s2], items[s1]
    return items

def exchange_direction(items):  # 第二类邻域选择，随机交换某个物品的方向
    s = random.randint(0, len(items) - 1)
    item = items[s]
    s_1, s_2 = random.randint(0, len(item) - 1), random.randint(0, len(item) - 1)
    while s_1 == s_2:
        s_2 = random.randint(0, len(item) - 1)
    item[s_1], item[s_2], = item[s_2], item[s_1]
    items[s] = item
    return items


def exchange_direction1(items):  # 随机交换侧放物品
    s = random.randint(0, len(items) - 1)
    item = items[s]
    s_1, s_2 = random.randint(1, len(item) - 1), random.randint(1, len(item) - 1)
    print(len(item))
    while s_1 == s_2:
        s_2 = random.randint(1, len(item) - 1)
    item[s_1], item[s_2] = item[s_2], item[s_1]
    items[s] = item
    return items

def Search(alpha, t_set, goods_se, boxs_se, markovlen):
    # alpha = 0.99
    # t = (1, 100)
    # m = 100
    # min_t = t_set[0]
    # t = t_set[1]
    L_box, L_goods, L_coordinates, num_select_min = OBT_3d(boxs_se, goods_se)
    # for i in range(len(L_coordinates)):
    #     print(len(L_goods[i]), L_coordinates)
    # show_3d(L_box, L_coordinates)
    # print(L_coordinates[0][-1])
    # print(L_box)
    print('good_check', goods_check(goods_se, L_goods))
    # 订单1
    L_0_boxmax = []
    L_1_boxmax = []
    L_2_boxmax = []
    for L_coordinates_list in L_coordinates:
        if L_coordinates_list and L_coordinates_list[-1]:
            for L_coordinates_list_j in L_coordinates_list:
                L_0_boxmax.append(L_coordinates_list_j[0] + L_coordinates_list_j[3])
                L_1_boxmax.append(L_coordinates_list_j[1] + L_coordinates_list_j[4])
                L_2_boxmax.append(L_coordinates_list_j[2] + L_coordinates_list_j[5])
    for L_list_box in L_box:
        L_list_box[0] = max(L_0_boxmax)
        L_list_box[1] = max(L_1_boxmax)
        L_list_box[2] = max(L_2_boxmax)
    print(len(L_box))
    # show_3d(L_box, L_coordinates)
    V_All_Box = L_box[0][0] * L_box[0][1] * L_box[0][2] * len(L_box)
    space_ratio = []
    for space_i in L_goods:
        space_good_sum = 0
        for space_j in space_i:
            space_good = space_j[0] * space_j[1] * space_j[2]
            space_good_sum += space_good
        space_ratio.append(space_good_sum / (L_box[0][0] * L_box[0][1] * L_box[0][2]))
    print('space_ratio:', space_ratio)
    print('all_space_ratio:', sum(space_ratio)/len(L_box))  # 装箱空间利用率
    for i in range(len(L_coordinates)):
        four_good, seven_good, nine_good = 0, 0, 0
        for j in range(len(L_coordinates[i])):
            if L_coordinates[i][j][0] == 21:
                four_good += 1
            elif L_coordinates[i][j][0] == 25:
                seven_good += 1
            elif L_coordinates[i][j][0] == 27.5:
                nine_good += 1
        # print(i, four_good, seven_good, nine_good)
    return V_All_Box, L_box, L_coordinates, num_select_min

    # 分析 订单2
    # L_0_boxmax = []
    # L_1_boxmax = []
    # L_2_boxmax = []
    # for i in range(len(L_coordinates)):
    #     L_0_boxmax.append(L_coordinates[i][-1][0] + L_coordinates[i][-1][3])
    #     L_1_boxmax.append(L_coordinates[i][-1][1] + L_coordinates[i][-1][4])
    #     L_2_boxmax.append(L_coordinates[i][-1][2] + L_coordinates[i][-1][5])
    # for L_list_box in L_box:
    #     L_list_box[0] = max(L_0_boxmax)
    #     L_list_box[1] = max(L_1_boxmax)
    #     L_list_box[2] = max(L_2_boxmax)
    # print(L_box)
    # show_3d(L_box, L_coordinates)
    # space_ratio = []
    # for space_i in L_goods:
    #     space_good_sum = 0
    #     for space_j in space_i:
    #         space_good = space_j[0] * space_j[1] * space_j[2]
    #         space_good_sum += space_good
    #     space_ratio.append(space_good_sum / (L_box[0][0] * L_box[0][1] * L_box[0][2]))
    # print('space_ratio:', space_ratio)
    # print('all_space_ratio:', sum(space_ratio)/len(L_box))  # 装箱空间利用率
    # for i in range(len(L_coordinates)):
    #     four_good, seven_good, nine_good = 0, 0, 0
    #     for j in range(len(L_coordinates[i])):
    #         if L_coordinates[i][j][0] == 21:
    #             four_good += 1
    #         elif L_coordinates[i][j][0] == 25:
    #             seven_good += 1
    #         elif L_coordinates[i][j][0] == 27.5:
    #             nine_good += 1
    #     print(i, four_good, seven_good, nine_good)

    # valuecurrent = len(L_box)
    # valuebest = valuecurrent
    # itemscurrent = goods_se
    # result = []  # 记录迭代过程中的最优解
    # while t > min_t:
    #     for i in range(markovlen):
    #         # 倒序+插段
    #         if random.random() > 0.5:  # 交换路径中的这2个节点的顺序
    #             itemsnew = exchange_item(goods_se)
    #         else:  # 交换次序
    #             itemsnew = exchange_direction(goods_se)
    #
    #         L_box, L_goods, L_coordinates = OBT_3d(boxs_se, itemsnew)
    #         # print(L_box, L_coordinates)
    #         space_ratio = []
    #         for space_i in L_goods:
    #             space_good_sum = 0
    #             for space_j in space_i:
    #                 space_good = space_j[0] * space_j[1] * space_j[2]
    #                 space_good_sum += space_good
    #             space_ratio.append(space_good_sum / (80 * 60 * 60))
    #         print('space_ratio:', space_ratio)  # 装箱空间利用率
    #
    #         valuenew = len(L_box)
    #         select_items = L_goods
    #         # print (valuenew)
    #         if valuenew >= valuecurrent:  # 接受该解
    #             r = 0
    #             # 更新solutioncurrent 和solutionbest
    #             valuecurrent = valuenew
    #             itemscurrent = itemsnew.copy()
    #             if valuenew >= valuebest:
    #                 valuebest = valuenew
    #                 itemsbest = select_items.copy()
    #         else:  # 按一定的概率接受该解
    #             if random.random() <= math.exp(-(valuecurrent - valuenew) / t):
    #                 # if np.random.rand() < (2/math.pi) * math.atan((valuenew - valuecurrent) * 0.000001*t):
    #                 valuecurrent = valuenew
    #                 itemscurrent = itemscurrent.copy()
    #             else:
    #                 itemsnew = itemscurrent.copy()
    #         t = alpha * t
    #     # result.append(itemsbest)
    #         print('temp:', t)
    #         print('itemsbest', itemsbest)
    #         print('valuebest', valuebest)
    # # show_3d(L_box, L_coordinates)


if __name__ == "__main__":
    space_ratio = []
    # 生成箱子集和商品集，计算并展示
    # 订单1
    boxs = [[79, 56, 18] for _ in range(20)]
    goods = [[21, 14, 9] for _ in range(2 + 5 + 7 + 15)]  # 选4号
    goods.extend([[25, 15, 9.5] for _ in range(25 + 25 + 25 + 25 + 25)])  # 选7号
    goods.extend([[27.5, 17.5, 10.5] for _ in range(25 + 25 + 22 + 20 + 10)])  # 选9号
    valuecurrent, L_box, L_coordinates, num_select_min = Search(alpha=0.99, t_set=(0.001, 1), goods_se=goods, boxs_se=boxs, markovlen=1)
    # 订单2
    # boxs = [[76, 36, 58] for _ in range(20)]
    # goods = [[21, 14, 9] for _ in range(4 + 10 + 10 + 15)]  # 选4号
    # goods.extend([[25, 15, 9.5] for _ in range(25 + 28 + 33 + 25 + 20)])  # 选7号
    # goods.extend([[27.5, 17.5, 10.5] for _ in range(35 + 30 + 26 + 24 + 15)])  # 选9号
    # valuecurrent, L_box, L_coordinates, num_select_min = Search(alpha=0.99, t_set=(0.001, 1), goods_se=goods, boxs_se=boxs, markovlen=1)
    valuebest_first = valuecurrent
    valuebest = valuecurrent
    print('valuebest:', valuebest)
    alpha, markovlen = 0.99, 1
    min_t, t = 0.001, 1
    while t > min_t:
        for i in range(markovlen):
            if random.random() > 0.5:  # 交换路径中的这2个节点的顺序
                goods = exchange_direction1(goods)
            boxs = boxs_generate_3d(nums_box=20, max_l_box=80, min_l_box=28, max_w_box=60, min_w_box=18,
                                    max_h_box=60, min_h_box=11)
            goods = [[21, 14, 9] for _ in range(2 + 5 + 7 + 15)]  # 选4号
            goods.extend([[25, 15, 9.5] for _ in range(25 + 25 + 25 + 25 + 25)])  # 选7号
            goods.extend([[27.5, 17.5, 10.5] for _ in range(25 + 25 + 22 + 20 + 10)])  # 选9号
            valuenew, L_box, L_coordinates, num_select_min = Search(alpha=0.99, t_set=(0.001, 1), goods_se=goods, boxs_se=boxs, markovlen=1)
            if valuenew <= valuecurrent:  # 接受该解
                valuecurrent = valuenew
                if valuenew <= valuebest:
                    valuebest = valuenew
            else:  # 按一定的概率接受该解
                if random.random() < math.exp(-(valuecurrent - valuenew) * 0.000001 / t):
                    valuecurrent = valuenew
            t = alpha * t
            print('valuebest:', valuebest)
            if (valuebest < valuebest_first - 777) and num_select_min >= 0:
                show_3d(L_box, L_coordinates)
                break
        if (valuebest < valuebest_first - 777) and num_select_min >= 0:
            break
