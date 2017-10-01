#!/user/bin/env python
# -*- coding: utf-8 -*-
import pyximport; pyximport.install()
from pydbm.dbm.interface.dbm_builder import DBMBuilder
from pydbm.neuron.visible_neuron import VisibleNeuron
from pydbm.neuron.hidden_neuron import HiddenNeuron
from pydbm.neuron.feature_point_neuron import FeaturePointNeuron
from pydbm.approximation.contrastive_divergence import ContrastiveDivergence
from pydbm.synapse.complete_bipartite_graph import CompleteBipartiteGraph
from pydbm.dbm.restricted_boltzmann_machines import RestrictedBoltzmannMachine


class DBM3LayerBuilder(DBMBuilder):
    '''
    GoFのデザイン・パタンの「Builder Pattern」の「具体的建築者」
    3層の制限ボルツマンマシンを組み立てることで、
    深層ボルツマンマシンのオブジェクトを生成する
    '''
    # 可視層ニューロンのリスト
    __visual_neuron_list = []
    # 特徴点の疑似可視層ニューロン
    __feature_point_neuron = []
    # 隠れ層ニューロンのリスト
    __hidden_neuron_list = []
    # グラフ
    __graph_list = []
    # 制限ボルツマンマシンのリスト
    __rbm_list = []
    # 学習率、具象プロパティ
    __learning_rate = 0.5

    def get_learning_rate(self):
        ''' getter '''
        if isinstance(self.__learning_rate, float) is False:
            raise TypeError()
        return self.__learning_rate

    def set_learning_rate(self, value):
        ''' setter '''
        if isinstance(value, float) is False:
            raise TypeError()
        self.__learning_rate = value

    learning_rate = property(get_learning_rate, set_learning_rate)

    def __init__(self):
        '''
        初期化する
        '''
        self.__visual_neuron_list = []
        self.__feature_point_neuron = []
        self.__hidden_neuron_list = []
        self.__graph_list = []
        self.__rbm_list = []

    def visible_neuron_part(self, activating_function, neuron_count):
        '''
        インターフェイスの実現
        可視層ニューロンを構築する

        Args:
            activating_function:    活性化関数
            neuron_count:           ニューロン数
        '''
        for i in range(neuron_count):
            visible_neuron = VisibleNeuron()
            visible_neuron.activating_function = activating_function
            visible_neuron.bernoulli_flag = True
            self.__visual_neuron_list.append(visible_neuron)

    def feature_neuron_part(self, activating_function, neuron_count):
        '''
        特徴点となる
        インターフェイスの実現
        n層のニューロンを構築する
        n-1層との連携では隠れ層として、n+1層との連携では疑似的な可視層として振る舞う

        Args:
            activating_function:    活性化関数
            neuron_count:           ニューロン数
        '''

        for i in range(neuron_count):
            feature_point_neuron = FeaturePointNeuron(VisibleNeuron())
            feature_point_neuron.activating_function = activating_function
            self.__feature_point_neuron.append(feature_point_neuron)

    def hidden_neuron_part(self, activating_function, neuron_count):
        '''
        インターフェイスの実現
        隠れ層ニューロンを構築する

        Args:
            activating_function:    活性化関数
            neuron_count:           ニューロン数
        '''

        for i in range(neuron_count):
            hidden_neuron = HiddenNeuron()
            hidden_neuron.activating_function = activating_function
            self.__hidden_neuron_list.append(hidden_neuron)

    def graph_part(self, approximate_interface):
        '''
        インターフェイスの実現
        完全二部グラフを構築する

        Args:
            approximate_interface:       近似用のオブジェクト
        '''

        self.__graph_list.append(CompleteBipartiteGraph())
        self.__graph_list.append(CompleteBipartiteGraph())

        self.__graph_list[0].create_node(
            self.__visual_neuron_list,
            self.__feature_point_neuron
        )
        self.__graph_list[1].create_node(
            self.__feature_point_neuron,
            self.__hidden_neuron_list
        )

    def get_result(self):
        '''
        インターフェイスの実現
        構築した制限ボルツマンマシンを返す

        Returns:
            制限ボルツマンマシンのオブジェクトのリスト

        '''
        for graph in self.__graph_list:
            rbm = RestrictedBoltzmannMachine(
                graph,
                self.__learning_rate,
                ContrastiveDivergence()
            )
            self.__rbm_list.append(rbm)

        return self.__rbm_list
