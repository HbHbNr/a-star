from a_star import Node, Matrix, MatrixAStar, readinputfile
from typing import List


def weightsstring2weights(weightsstring: str) -> List[List[int]]:
    weights: List[List[int]] = [list(map(int, list(row))) for row in weightsstring.split(',')]
    return weights


def test_2x2():
    weightsstring = '12,13'
    startNode = Node(1, 1)
    targetNode = Node(2, 2)
    matrix = Matrix(weightsstring2weights(weightsstring))

    assert MatrixAStar.findPath(matrix, startNode, targetNode) == 4


def test_3x3():
    weightsstring = '116,138,213'
    startNode = Node(1, 1)
    targetNode = Node(3, 3)
    matrix = Matrix(weightsstring2weights(weightsstring))

    assert MatrixAStar.findPath(matrix, startNode, targetNode) == 7


def test_4x3():
    weightsstring = '1163,1381,2136'
    startNode = Node(1, 1)
    targetNode = Node(4, 3)
    matrix = Matrix(weightsstring2weights(weightsstring))

    assert MatrixAStar.findPath(matrix, startNode, targetNode) == 13


def test_aoc2021_day15_example():
    inputfile = 'inputfiles/aoc2021_day15_example.txt'
    weights = readinputfile(inputfile)
    startNode = Node(1, 1)
    targetNode = Node(len(weights[0]), len(weights))
    matrix = Matrix(weights)

    assert MatrixAStar.findPath(matrix, startNode, targetNode) == 40


def test_aoc2021_day15_input():
    inputfile = 'inputfiles/aoc2021_day15_input.txt'
    weights = readinputfile(inputfile)
    startNode = Node(1, 1)
    targetNode = Node(len(weights[0]), len(weights))
    matrix = Matrix(weights)

    assert MatrixAStar.findPath(matrix, startNode, targetNode) == 458
