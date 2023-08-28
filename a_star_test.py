from a_star import Node, Matrix, Matrix5x5, MatrixAStar, readinputfile
from typing import List


def weightsstring2weights(weightsstring: str) -> List[List[int]]:
    weights: List[List[int]] = [list(map(int, list(row))) for row in weightsstring.split(',')]
    return weights


def test_2x2():
    weightsstring = '12,13'
    startNode = Node(0, 0)
    targetNode = Node(1, 1)
    matrix = Matrix(weightsstring2weights(weightsstring))

    assert MatrixAStar.findPath(matrix, startNode, targetNode) == 4


def test_3x3():
    weightsstring = '116,138,213'
    startNode = Node(0, 0)
    targetNode = Node(2, 2)
    matrix = Matrix(weightsstring2weights(weightsstring))

    assert MatrixAStar.findPath(matrix, startNode, targetNode) == 7


def test_4x3():
    weightsstring = '1163,1381,2136'
    startNode = Node(0, 0)
    targetNode = Node(3, 2)
    matrix = Matrix(weightsstring2weights(weightsstring))

    assert MatrixAStar.findPath(matrix, startNode, targetNode) == 13


def test_aoc2021_day15a_example():
    inputfile = 'inputfiles/aoc2021_day15_example.txt'
    weights = readinputfile(inputfile)
    startNode = Node(0, 0)
    targetNode = Node(len(weights[0]) - 1, len(weights) - 1)
    matrix = Matrix(weights)

    assert MatrixAStar.findPath(matrix, startNode, targetNode) == 40


def test_aoc2021_day15a_input():
    inputfile = 'inputfiles/aoc2021_day15_input.txt'
    weights = readinputfile(inputfile)
    startNode = Node(0, 0)
    targetNode = Node(len(weights[0]) - 1, len(weights) - 1)
    matrix = Matrix(weights)

    assert MatrixAStar.findPath(matrix, startNode, targetNode) == 458


def test_aoc2021_day15b_example():
    inputfile = 'inputfiles/aoc2021_day15_example.txt'
    weights = readinputfile(inputfile)
    startNode = Node(0, 0)
    targetNode = Node(len(weights[0]) * 5 - 1, len(weights) * 5 - 1)
    matrix = Matrix(weights)
    matrix5x5 = Matrix5x5(matrix)

    assert MatrixAStar.findPath(matrix5x5, startNode, targetNode) == 315


def test_aoc2021_day15b_input():
    inputfile = 'inputfiles/aoc2021_day15_input.txt'
    weights = readinputfile(inputfile)
    startNode = Node(0, 0)
    targetNode = Node(len(weights[0]) * 5 - 1, len(weights) * 5 - 1)
    matrix = Matrix(weights)
    matrix5x5 = Matrix5x5(matrix)

    assert MatrixAStar.findPath(matrix5x5, startNode, targetNode) == 2800
