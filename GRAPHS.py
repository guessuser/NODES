import pygame
from pygame.draw import circle

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1500, 750))


# цвета
COLOR = {'Black':(0, 0, 0), 'Red':0xFF0000, 'Blue':0x0000FF, 'Yellow':0xFFC91F,
          'Green': 0x00FF00, 'Magenta': 0xFF03B8, 'Cyan': 0x00FFCC, 'Grey': 0x7D7D7D, 'White': 0xFFFFFF}

# обратный список цветов, который используется для сохранения в файл
COLOR_Save = {(0, 0, 0):'Black', 0xFF0000:'Red', 0x0000FF:'Blue', 0xFFC91F:'Yellow',
          0x00FF00:'Green', 0xFF03B8:'Magenta', 0x00FFCC:'Cyan', 0x7D7D7D:'Grey', 0xFFFFFF:'White'}

SIZE = {'Small': 16, 'Medium': 32, 'Big': 64}


# ПАРАМЕТРЫ КНОПОК
# 1) кортеж с размерами кнопки
# 2) кортеж с координатами кнопки
# 3) надпись на кнопке
buttons_parametrs = (  ((60,30), (50,5), 'Node'),          ((60,30), (140,5), 'Edge'),
                       ((120,30), (250,5), 'Move Node'),
                       ((120,30), (450,5), 'Del Node'),    ((120,30), (580,5), 'Del Edge'),
                       ((60,30), (760,5), 'Color'),        ((60,30), (880,5), 'Size'),
                       ((120,30), (1060,5), 'Save Graph'), ((120,30), (1230,5), 'Add Graph'),
                       ((60,30), (1400,5), 'Clear'),       ((60,30), (5,5), 'Menu'),

                       ((60,30), (130,5), 'Red'),          ((60,30), (190,5), 'Blue'),
                       ((90,30), (250,5), 'Yellow'),       ((80,30), (330,5), 'Green'),
                       ((90,30), (410,5), 'Magenta'),      ((60,30), (510,5), 'Cyan'),
                       ((60,30), (580,5), 'Grey'),

                       ((60,30), (90,5), 'Small'),        ((90,30), (160,5), 'Medium'),
                       ((60,30), (250,5), 'Big'))


# генератор кнопок
buttons = []
for i in buttons_parametrs:
    button = pygame.Surface(i[0], pygame.SRCALPHA)
    FONT = pygame.font.Font(None, 30).render(i[2], True, COLOR['Black'])
    button.blit(FONT, (5, 5))
    buttons.append((button, i[1]))


# генератор номеров узлов
numbers = []
for i in range(1,1000):
    surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    number = pygame.font.Font(None, 30).render(str(i), True, COLOR['Black'])
    surface.blit(number, (0,0))
    numbers.append(surface)


# Словарь узлов
# ключ - номер узла (натуратьное число тип int), под ключем лежит словарь с тремя параметрами узла:
    # 'pos' - кортеж (x,y)
    # 'color' - цвет из словаря COLOR
    # 'size' - число из словаря SIZE
nodes = dict()

# список ребер состоящий из кортежей с номерами узлов (N1, N2)
edges = []

# определяет нажатую кнопку и выполняет соответствующее действие
def press_button(pos, buttons, buttons_parametrs, nodes, edges, graph, color_size_default):

    # если основное меню возвращает выбранный режим
    if mode == 'start':
        a = -1
        for i in range(7):
            if (buttons[i][1][0] < pos[0] < buttons[i][1][0]+buttons_parametrs[i][0][0]) and (5 < pos[1] < 35):
                a = 1
                return buttons_parametrs[i][2]
        for i in range(7,10):
            if (buttons[i][1][0] < pos[0] < buttons[i][1][0]+buttons_parametrs[i][0][0]) and (5 < pos[1] < 35):
                graph[i-7](nodes, edges)
                a = 1
                return 'start'
        if a == -1:
            return 'start'

    # если режим выбор цвета, меняет цвет по умолчанию
    elif mode == 'Color':
        for i in range(11, 18):
            if (buttons[i][1][0] < pos[0] < buttons[i][1][0]+buttons_parametrs[i][0][0]) and (5 < pos[1] < 35):
                color_size_default['color'] = COLOR[buttons_parametrs[i][2]]

    # если режим выбор размера, меняет размер по умолчанию
    elif mode == 'Size':
        for i in range(18, 21):
            if (buttons[i][1][0] < pos[0] < buttons[i][1][0]+buttons_parametrs[i][0][0]) and (5 < pos[1] < 35):
                color_size_default['size'] = SIZE[buttons_parametrs[i][2]]


# возвращает номер нажатого узла, или -1
def press_node(pos, nodes, empty):
    for i in nodes:
        if (pos[0]-nodes[i]['pos'][0])**2+(pos[1]-nodes[i]['pos'][1])**2 <= nodes[i]['size']**2:
            return i
    return empty


# рисует кнопки на экране
def show_buttons(mode, buttons, screen):
    if mode == 'start':
        for i in range(10):
            screen.blit(buttons[i][0], buttons[i][1])
    elif mode == 'Color':
        for i in range(11, 18):
            screen.blit(buttons[i][0], buttons[i][1])
        screen.blit(buttons[10][0], buttons[10][1])
    elif mode == 'Size':
        for i in range(18, 21):
            screen.blit(buttons[i][0], buttons[i][1])
        screen.blit(buttons[10][0], buttons[10][1])
    else:
        screen.blit(buttons[10][0], buttons[10][1])


# рисует граф на экране
def show_graph(edges, nodes, numbers, COLORS, screen):

    # рисует рёбра
    for edge in edges:
        pygame.draw.line(screen, COLORS['Black'], nodes[edge[0]]['pos'], nodes[edge[1]]['pos'], 1)

    # рисует узлы, и номера на них
    for i in nodes:
        circle(screen, nodes[i]['color'], nodes[i]['pos'], nodes[i]['size'])
        screen.blit(numbers[i], (nodes[i]['pos'][0]-9,nodes[i]['pos'][1]-8))


# перемещает узел
def move_node(pos, nodes, movable_node, not_exist):

    # проверка на клик в доступную зону
    click_in_screen = (pos[0] > 50) and (pos[0] < 1450) and (pos[1] < 700) and (pos[1] > 50)

    # 1) если передвигаемый узел не существует, фунция возвращает в него нажытый или пустой узел (-1)
    # 2) если передвигаемый узел не не существует, и клик в актиной зоне, задаёт новые координаты узла
    # 3) если клик на кнопку Menu, возвращает пустой
    if movable_node is not_exist:
        return press_node(pos, nodes, not_exist)
    elif (movable_node is not not_exist) and click_in_screen:
        nodes[movable_node]['pos'] = pos
        return not_exist
    elif (5 < pos[0] < 65) and (5 < pos[1] < 35):
        return not_exist


# сохраняет граф в файл
def save_graph(nodes, edges):
    with open('saved_graph.txt', 'w') as f:

        # первое число это кол-во узлов
        f.write(str(len(nodes))+' ')

        # записывает в строку все параметры всех узлов через пробел
        for i in nodes:
            f.write(str(i) + ' ' + str(nodes[i]['pos'][0]) + ' ' + str(nodes[i]['pos'][1])
                    + ' ' + COLOR_Save[nodes[i]['color']] + ' ' + str(nodes[i]['size']) + ' ')

        # вторая строка
        f.write('\n')

        # первое число это кол-во рёбер
        f.write(str(len(edges))+' ')

        # записывает в строку координаты всех рёбер через пробел
        for edge in edges:
            f.write(str(edge[0])+' '+str(edge[1])+' ')


# рисует граф из файла
def add_graph(nodes, edges):

    # очищаем уже нарисованный граф
    clear_screen(nodes, edges)
    with open('saved_graph.txt', 'r') as f:

        # соотвественно списки узлов и рёбер
        nodes_str = f.readline().split()
        edges_str = f.readline().split()

    # записывает все узлы с их параметрами в словарь узлов
    for i in range(int(nodes_str[0])):
        nodes[int(nodes_str[5*i+1])] = {'pos': (int(nodes_str[5*i+2]), int(nodes_str[5*i+3])),
                                        'color': COLOR[nodes_str[5*i+4]],  'size': int(nodes_str[5*i+5])}

    # записывает все координаты рёбер в список рёбер
    for i in range(int(edges_str[0])):
        edges.append((int(edges_str[2*i+1]), int(edges_str[2*i+2])))


# стирает все с экрана
def clear_screen(nodes, edges):
    nodes.clear()
    edges.clear()


# создаёт новый узел
def add_node(pos, nodes, color_size):
    click_in_screen = (pos[0] > 50) and (pos[0] < 1450) and (pos[1] < 700) and (pos[1] > 50)

    if click_in_screen:
        if len(nodes) != 0:
            node = {'pos': (pos[0], pos[1]),  'color': color_size['color'],  'size': color_size['size']}
            nodes[max(list(nodes.keys()))+1] = node
        else:
            node = {'pos': (pos[0], pos[1]),  'color': color_size['color'],  'size': color_size['size']}
            nodes[0] = node


# удаляет узел
def del_node(pos, nodes, edges, not_exist):
    removed_node = press_node(pos, nodes, not_exist)
    if removed_node != not_exist:

        # удаляет узел
        nodes.pop(removed_node)

        # удаляет все рёбра связанные с этим узлом
        for i in range( sum([edge.count(removed_node) for edge in edges]) ):
            for edge in edges:
                if removed_node in edge:
                    edges.remove(edge)
                    break


# вспомогательные переменные
not_exist = -1
edge_start = not_exist
edge_end = not_exist
movable_node = not_exist
graph = [save_graph, add_graph, clear_screen]
color_size_default = {'color':COLOR['Yellow'], 'size':SIZE['Small']}


mode = 'start'
finished = False

# осуществляет возвращение в главное меню при нажатии кнопки Menu
def menu(pos):
    global mode
    if (5 < pos[0] < 65) and (5 < pos[1] < 35):
        mode = 'start'

while not finished:
    screen.fill(COLOR['White'])

    show_buttons(mode, buttons, screen)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            finished = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            menu(pos)

            if mode == 'start':
                mode = press_button(pos, buttons, buttons_parametrs, nodes, edges, graph, color_size_default)

            elif mode == 'Node':
                add_node(pos, nodes, color_size_default)

            elif mode == 'Edge':
                edge_start = press_node(pos, nodes, not_exist)
                if (edge_start != not_exist):
                    mode = 'Edge2'

            elif mode == 'Edge2':
                edge_end = press_node(pos, nodes, not_exist)
                if (edge_end != not_exist) and (edge_end != edge_start):
                    edges.append((edge_start, edge_end))
                    mode = 'Edge'
                    edge_start = not_exist
                    edge_end = not_exist

            elif mode == 'Move Node':
                movable_node = move_node(pos, nodes, movable_node, not_exist)

            elif mode == 'Del Node':
                del_node(pos, nodes, edges, not_exist)

            elif mode == 'Del Edge':
                edge_start = press_node(pos, nodes, not_exist)
                if edge_start != not_exist:
                    for i in edges:
                        if edge_start in i:
                            mode = 'Del Edge2'

            elif mode == 'Del Edge2':
                edge_end = press_node(pos, nodes, not_exist)
                if (edge_end != not_exist) and (edge_start != edge_end):
                    for i in edges:
                        if (edge_start in i) and (edge_end in i):
                            edges.remove(i)
                    mode = 'Del Edge'

            elif mode == 'Color':
                press_button(pos, buttons, buttons_parametrs, nodes, edges, graph, color_size_default)
                color_node = press_node(pos, nodes, not_exist)
                if color_node != not_exist:
                    nodes[color_node]['color'] = color_size_default['color']

            elif mode == 'Size':
                press_button(pos, buttons, buttons_parametrs, nodes, edges, graph, color_size_default)
                color_node = press_node(pos, nodes, not_exist)
                if color_node != not_exist:
                    nodes[color_node]['size'] = color_size_default['size']


    show_graph(edges, nodes, numbers, COLOR, screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()