# -*- coding: utf-8 -*-

# python imports
from math import degrees

# pyfuzzy imports
from fuzzy.storage.fcl.Reader import Reader


class FuzzyController:

    def __init__(self, fcl_path):
        self.system = Reader().load_from_file(fcl_path)


    def _make_input(self, world):
        return dict(
            cp = world.x,
            cv = world.v,
            pa = degrees(world.theta),
            pv = degrees(world.omega)
        )


    def _make_output(self):
        return dict(
            force = 0.
        )

    def p(x, a, b, c):
        if (x>=a and x<=b and a!=None):
            return (1/(b-a))*(x-a)
        if (x>=b and x<=c and c!=None):
            return (-1/(c-b))*(x-c)
        return 0

    def calculate_pv(x):
        pv = dict()
        pv["cw_fast"] = p(x, None, -200, -100)
        pv["cv_slow"] = p(x, -200, -100, 0)
        pv["stop"] = p(x, -100, 0, 100)
        pv["ccw_slow"] = p(x, 0, 100, 200)
        pv["ccw_fast"] = p(x, 100, 200, None)
        return pv

    def calulate_pa(x):
        pa = dict()
        pa["up_more_right"] = p(x, 0, 30, 60)
        pa["up_right"] = p (x, 30, 60, 90)
        pa["up"] = p(x, 60, 90, 120)
        pa["up_left"] = p(x, 90, 120, 150)
        pa["up_more_left"] = p(x, 120, 150, 180)
        pa["down_more_left"] = p(x, 180, 210, 240)
        pa["down_left"] = p(x, 210, 240, 270)
        pa["down"] = p(x, 240, 270, 300)
        pa["down_right"] = p(x, 270, 300, 330)
        pa["down_more_right"] = p(x, 300, 330, 360)
        return pa

    def calculate_cp(x):
        cp = dict()
        cp["left_far"] = p(x, None, -10, -5)
        cp["left_near"] = p(x, -10, -2.5, 0)
        cp["stop"] = p(x, -2.5, 0, 2.5)
        cp["right_near"] = p(x, 0, 2.5, 10)
        cp["right_far"] = p(x, 5, 10, None)
        return cp

    def calculate_cv(x):
        cv = dict()
        cv["left_fast"] = p(x, None, -5, -2.5)
        cv["left_slow"] = p(x, -5, -1, 0)
        cv["stop"] = p(x, -1, 0, 1)
        cv["right_slow"] = p(x, 0, 1, 5)
        cv["right_fast"] = p(x, 2..5, 5, None)
        return cv

    def defuzzy_force(x): 
        force = dict()
        force["left_fast"] = p(x, -100, -80, -60)
        force["left_slow"] = p(x, -80, -60, 0)
        force["stop"] = p(x, -60, 0, 60)
        force["right_slow"] = p(x, 0, 60, 80)
        force["right_fast"] = p(x, 60, 80, 100)
        return force

    def calculate_force(world):
        input = self._make_input(world)
        pv_dict = calculate_pv(input.pv)
        cp_dict = calculate_cp(input.cp)
        pa_dict = calculate_pa(input.pa)
        cv_dict = calculate_cv(input.cv)

        force = dict()
        force["left_fast"] = 0
        force["left_slow"] = 0
        force["stop"] = 0
        force["right_slow"] = 0
        force["right_fast"] = 0

        force["stop"] = max(force["stop"], max(min(pa_dict["up"] , pv_dict["stop"]), min(pa_dict["up_right"], pv_dict["ccw_slow"]), min(pa["up_left"], pv["cw_slow"])))

        force["right_fast"] = max(force["right_fast"], min(pa_dict["up_more_right"], pv_dict["ccw_slow"]))

        force["right_fast"] = max(force["right_fast"], min(pa_dict["up_more_right"], pv_dict["cw_slow"]))

        force["left_fast"] = max(force["left_fast"], min(pa_dict["up_more_left"], pv_dict["cw_slow"]))

        force["left_fast"] = max(force["left_fast"], min(pa_dict["up_more_left"], pv_dict["ccw_slow"]))

        force["left_slow"] = max(force["left_slow"],min(pa_dict["up_more_right"], pv["ccw_fast"]))

        force["right_fast"] = max(force["right_fast"], min(pa_dict["up_more_right"], pv_dict["cw_fast"]))

        force["right_slow"] = max(force["right_slow"], min(pa_dict["up_more_left"], pv_dict["cw_fast"]))

        force["left_fast"] = max(force["left_fast"], min(pa_dict["up_more_left"], pv_dict["ccw_fast"]))

        force["right_fast"] = max(force["right_fast"],min(pa_dict["down_more_right"], pv_dict["ccw_slow"]))

        force["stop"] = max(force["stop"], min(pa_dict["down_more_right"], pv_dict["cw_slow"]))

        force["left_fast"] = max(force["left_fast"], min(pa_dict["down_more_left"], pv_dict["cw_slow"]))

        force["stop"] = max(force["stop"], min(pa_dict["down_more_left"], pv_dict["ccw_slow"]))

        force["stop"] = max(force["stop"], min(pa_dict["down_more_right"], pv["ccw_fast"]))

        force["stop"] = max(force["stop"], min(pa_dict["down_more_right"], pv_dict["cw_fast"]))

        force["stop"] = max(force["stop"], min(pa_dict["more_down_left"], pv_dict["cw_fast"]))

        force["stop"] = max(force["stop"], min(pa_dict["down_more_left"], pv_dict["ccw_fast"]))

        force["right_fast"] = max(force["right_fast"], min(pa_dict["down_right"], pv_dict["ccw_slow"]))

        force["right_fast"] = max(force["right_fast"], min(pa_dict["down_right"], pv_dict["cw_slow"]))

        force["left_fast"] = max(force["left_fast"], min(pa_dict["down_left"], pv_dict["cw_slow"]))

        force["left_fast"] = max(force["left_fast"], min(pa_dict["down_left"], pv_dict["ccw_slow"]))

        force["stop"] = max(force["stop"], min(pa_dict["down_right"], pv_dict["ccw_fast"]))

        force["right_slow"] = max(force["right_slow"], min(pa_dict["down_right"], pv_dict["cw_fast"]))

        force["stop"] = max(force["stop"], min(pa_dict["down_left"], pv_dict["cw_fast"]))

        force["left_slow"] = max(force["left_slow"], min(pa_dict["down_left"], pv_dict["ccw_fast"]))

        force["right_slow"] = max(force["right_slow"], min(pa_dict["up_right"], pv_dict["ccw_slow"]))

        force["right_fast"] = max(force["right_fast"], min(pa_dict["up_right"], pv_dict["cw_slow"]))

        force["right_fast"] = max(force["right_fast"], min(pa_dic["up_right"], pv_dict["right_fast"]))

        force["left_slow"] = max(force["left_slow"], min(pa_dict["up_left"], pv_dict["cw_slow"]))

        force["left_fast"] = max(force["left_fast"], min(pa_dict["up_left"], pv_dict["ccw_slow"]))

        force["left_fast"] = max(force["left_fast"], min(pa_dict["up_left"], pv_dict["stop"]))

        force["left_fast"] = max(force["left_fast"], min(pa_dict["up_right"], pv_dict["ccw_fast"]))

        force["right_fast"] = max(force["right_fast"], min(pa_dict["up_right"], pv_dict["cw_fast"]))

        force["right_fast"] = max(force["right_fast"], min(pa_dict["up_left"], pv_dict["cw_fast"]))

        force["left_fast"] = max(force["left_fast"], min(pa_dict["up_left"], pv_dict["ccw_fast"]))

        #35
        force["right_fast"] = max(force["right_fast"], min(pa_dict["down"], pv_dict["stop"]))

        force["stop"] = max(force["stop"], min(pa_dict["down"], pv_dict["cw_fast"]))

        force["stop"] = max(force["stop"], min(pa_dict["down"], pv_dict["ccw_fast"]))

        force["left_slow"] = max(force["left_slow"], min(pa_dict["up"], pv_dict["ccw_slow"]))

        force["left_fast"] = max(force["left_fast"], min(pa_dict["up"], pv_dict["ccw_fast"]))

        force["right_slow"] = max(force["right_slow"], min(pa_dict["up"], pv_dict["cw_slow"]))

        force["right_fast"] = max(force["right_fast"], min(pa_dict["up"], pv_dict["cw_fast"]))

        force["stop"] = max(force["stop"], min(pa_dict["up"], pv_dict["stop"]))

    def decide(self, world):
        # output is between -100 & 100 
        # for input use self._make_input(world)
        output = self._make_output()
        #self.system.calculate(self._make_input(world), output)

        return output['force']
