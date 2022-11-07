import numpy as np
import math
import matplotlib.pyplot as plt  # type: ignore
import matplotlib.patches as mpatches  # type: ignore
from anastruct.basic import find_nearest, rotate_xy
from anastruct.fem.plotter.values import (
    PlottingValues,
    det_scaling_factor,
    plot_values_axial_force,
    plot_values_bending_moment,
    plot_values_deflection,
    plot_values_element,
    plot_values_shear_force,
)

from typing import (
    Tuple,
    Union,
    List,
    Optional,
    Dict,
    Set,
    TYPE_CHECKING,
    Sequence,
    cast,
    Collection,
    Any,
)


PATCH_SIZE = 0.05


class Plotter(PlottingValues):
    def __init__(self, system, mesh):
        super(Plotter, self).__init__(system, mesh)
        self.system = system
        self.one_fig = None
        self.max_q = 0
        self.max_qn = 0
        self.max_system_point_load = 0

    def __start_plot(self, figsize):
        plt.close("all")
        self.fig = plt.figure(figsize=figsize)
        self.one_fig = self.fig.add_subplot(111)
        plt.tight_layout()

    def __fixed_support_patch(self, max_val):
        """
        :param max_val: max scale of the plot
        """
        width = height = PATCH_SIZE * max_val
        for node in self.system.supports_fixed:
            support_patch = mpatches.Rectangle(
                (node.vertex.x - width * 0.5, -node.vertex.z - width * 0.5),
                width,
                height,
                color='mistyrose',
                zorder=9,
            )
            self.one_fig.add_patch(support_patch)
        for node in self.system.supports_fixed:
            support_patch = mpatches.Rectangle(
                (node.vertex.x - width * 0.5, -node.vertex.z - width * 0.5),
                width,
                height,
                linewidth=0, fill=0,
                hatch='//////',
                zorder=9,
            )
            self.one_fig.add_patch(support_patch)

    def __hinged_support_patch(self, max_val):
        """
        :param max_val: max scale of the plot
        """
        radius = PATCH_SIZE * max_val
        for node in self.system.supports_hinged:
            support_patch = mpatches.RegularPolygon(
                (node.vertex.x, node.vertex.y - radius),
                numVertices=3,
                radius=radius,
                color="green",
                zorder=9,
                alpha=0.7,
            )
            self.one_fig.add_patch(support_patch)
        for node in self.system.supports_hinged:
            support_patch = mpatches.Circle(
                (node.vertex.x, node.vertex.y - radius),
                radius=radius/3,
                color="white",
                zorder=9,
            )
            self.one_fig.add_patch(support_patch)

    def __rotational_support_patch(self, max_val):
        """
        :param max_val: max scale of the plot
        """
        width = height = PATCH_SIZE * max_val
        for node in self.system.supports_rotational:
            support_patch = mpatches.Rectangle(
                (node.vertex.x - width * 0.5, -node.vertex.z - width * 0.5),
                width,
                height,
                color="r",
                zorder=9,
                fill=False,
            )
            self.one_fig.add_patch(support_patch)

    def __roll_support_patch(self, max_val):
        """
        :param max_val: max scale of the plot
        """
        radius = PATCH_SIZE * max_val
        count = 0
        for node in self.system.supports_roll:
            direction = self.system.supports_roll_direction[count]
            rotate = self.system.supports_roll_rotate[count]
            x1 = np.cos(np.pi) * radius + node.vertex.x + radius  # vertex.x
            z1 = np.sin(np.pi) * radius + node.vertex.y  # vertex.y
            x2 = (
                np.cos(np.radians(90)) * radius + node.vertex.x + radius
            )  # vertex.x + radius
            z2 = np.sin(np.radians(90)) * radius + node.vertex.y  # vertex.y + radius
            x3 = (
                np.cos(np.radians(270)) * radius + node.vertex.x + radius
            )  # vertex.x + radius
            z3 = np.sin(np.radians(270)) * radius + node.vertex.y  # vertex.y - radius

            triangle = np.array([[x1, z1], [x2, z2], [x3, z3]])

            if node.id in self.system.inclined_roll:
                angle = self.system.inclined_roll[node.id]
                triangle = rotate_xy(triangle, angle + np.pi * 0.5)
                support_patch = plt.Polygon(triangle, color="r", zorder=9)
                self.one_fig.add_patch(support_patch)
                self.one_fig.plot(
                    triangle[1:, 0] - 0.5 * radius * np.sin(angle),
                    triangle[1:, 1] - 0.5 * radius * np.cos(angle),
                    color="r",
                )
                if not rotate:
                    rect_patch = mpatches.RegularPolygon(
                        (node.vertex.x, node - node.vertex.y),
                        numVertices=4,
                        radius=radius,
                        orientation=angle,
                        color="r",
                        zorder=9,
                        fill=False,
                    )
                    self.one_fig.add_patch(rect_patch)

            elif direction == 2:  # horizontal roll
                support_patch = mpatches.RegularPolygon(
                    (node.vertex.x, node.vertex.y - radius),
                    numVertices=3,
                    radius=radius,
                    color="r",
                    zorder=9,
                    alpha=0.7
                )
                circle1 = mpatches.Circle((node.vertex.x-0.5*radius,-node.vertex.z-1.75*radius), radius=radius/4.,color="k")
                circle2 = mpatches.Circle((node.vertex.x+0.5*radius,-node.vertex.z-1.75*radius), radius=radius/4.,color="k")
                self.one_fig.add_patch(support_patch)
                self.one_fig.add_patch(circle1)
                self.one_fig.add_patch(circle2)
                y = -node.vertex.z - 2 * radius
                self.one_fig.plot(
                    [node.vertex.x - radius, node.vertex.x + radius], [y, y], color="r"
                )
                if not rotate:
                    rect_patch = mpatches.Rectangle(
                        (node.vertex.x - radius / 2, -node.vertex.z - radius / 2),
                        radius,
                        radius,
                        color="r",
                        zorder=9,
                        fill=False,
                    )
                    self.one_fig.add_patch(rect_patch)
            elif direction == 1:  # vertical roll
                # translate the support to the node

                support_patch = mpatches.Polygon(triangle, color="r", zorder=9)
                self.one_fig.add_patch(support_patch)

                y = node.vertex.y - radius
                self.one_fig.plot(
                    [node.vertex.x + radius * 1.5, node.vertex.x + radius * 1.5],
                    [y, y + 2 * radius],
                    color="r",
                )
                if not rotate:
                    rect_patch = mpatches.Rectangle(
                        (node.vertex.x - radius / 2, -node.vertex.z - radius / 2),
                        radius,
                        radius,
                        color="r",
                        zorder=9,
                        fill=False,
                        alpha=0.7
                    )
                    self.one_fig.add_patch(rect_patch)
            count += 1

    def __rotating_spring_support_patch(self, max_val):
        """
        :param max_val: max scale of the plot
        """
        radius = PATCH_SIZE * max_val

        for node, _ in self.system.supports_spring_y:
            r = np.arange(0, radius, 0.001)
            theta = 25 * np.pi * r / (0.2 * max_val)
            x = np.cos(theta) * r + node.vertex.x
            y = np.sin(theta) * r - radius + node.vertex.y
            self.one_fig.plot(x, y, color="r", zorder=9)

            # Triangle
            support_patch = mpatches.RegularPolygon(
                (node.vertex.x, node.vertex.y - radius * 3),
                numVertices=3,
                radius=radius * 0.9,
                color="r",
                zorder=9,
            )
            self.one_fig.add_patch(support_patch)

    def __spring_support_patch(self, max_val):
        """
        :param max_val: max scale of the plot
        """
        h = PATCH_SIZE * max_val
        left = -0.5 * h
        right = 0.5 * h
        dh = 0.2 * h

        for node, _ in self.system.supports_spring_z:
            yval = np.arange(0, -9, -1) * dh + node.vertex.y
            xval = (
                np.array([0, 0, left, right, left, right, left, 0, 0]) + node.vertex.x
            )

            self.one_fig.plot(xval, yval, color="r", zorder=10)

            # Triangle
            support_patch = mpatches.RegularPolygon(
                (node.vertex.x, -node.vertex.z - h * 2.6),
                numVertices=3,
                radius=h * 0.9,
                color="r",
                zorder=10,
            )
            self.one_fig.add_patch(support_patch)

        for node, _ in self.system.supports_spring_x:
            xval = np.arange(0, 9, 1) * dh + node.vertex.x
            yval = (
                np.array([0, 0, left, right, left, right, left, 0, 0]) + node.vertex.y
            )

            self.one_fig.plot(xval, yval, color="r", zorder=10)

            # Triangle
            support_patch = mpatches.RegularPolygon(
                (node.vertex.x + h * 1.7, -node.vertex.z - h),
                numVertices=3,
                radius=h * 0.9,
                color="r",
                zorder=10,
            )
            self.one_fig.add_patch(support_patch)

    def __q_load_patch(self, max_val, verbosity):
        """
        :param max_val: max scale of the plot

        xn1;yn1  q-load   xn1;yn1
        -------------------
        |__________________|
        x1;y1  element    x2;y2
        """

        def __plot_patch(h1, h2, x1, y1, x2, y2, ai, qi, q, direction, el_angle):

            # - value, because the positive z of the system is opposite of positive y of the plotter
            xn1 = x1 + np.sin(ai) * h1 * direction
            yn1 = y1 + np.cos(ai) * h1 * direction
            xn2 = x2 + np.sin(ai) * h2 * direction
            yn2 = y2 + np.cos(ai) * h2 * direction
            coordinates = ([x1, xn1, xn2, x2], [y1, yn1, yn2, y2])
            self.one_fig.plot(*coordinates, color="g")
            rec = plt.Polygon(np.vstack(coordinates).T, color="g", alpha=0.3)
            self.one_fig.add_patch(rec)

            if verbosity == 0:
                # arrow
                pos = np.sqrt(((y1 - y2) ** 2) + ((x1 - x2) ** 2))
                cg = ((pos / 3) * (qi + 2 * q)) / (qi + q)
                height = math.sin(el_angle) * cg
                base = math.cos(el_angle) * cg

                len_x1 = np.sin(ai - np.pi) * 0.6 * h1 * direction
                len_x2 = np.sin(ai - np.pi) * 0.6 * h2 * direction
                len_y1 = np.cos(ai - np.pi) * 0.6 * h1 * direction
                len_y2 = np.cos(ai - np.pi) * 0.6 * h2 * direction
                len_y1_c = -np.cos(ai - np.pi) * 0.6 * h1 * direction
                len_y2_c = -np.cos(ai - np.pi) * 0.6 * h2 * direction
                step_xb = np.linspace(x1, x2, 11)
                step_yb = np.linspace(y1, y2, 11)
                step_x = np.linspace(xn1, xn2, 11)
                step_y = np.linspace(yn1, yn2, 11)
                step_y_c = np.linspace(y1, y2, 11)
                step_len_x = np.linspace(len_x1, len_x2, 11)
                step_len_y = np.linspace(len_y1, len_y2, 11)
                step_len_y_c = np.linspace(len_y1_c, len_y2_c, 11)
                average_h = (h1 + h2) / 2
                # fc = face color, ec = edge color
                self.one_fig.text(xn1, yn1, f"q={np.round(10000*qi)/10000.0}", color="b", fontsize=9, zorder=10)
                self.one_fig.text(xn2, yn2, f"q={np.round(10000*q)/10000.0}", color="b", fontsize=9, zorder=10)

                # add multiple arrows to fill load
                for counter in range(len(step_x)):
                    if q + qi >= 0:
                        if counter == 0:
                            shape = "right"
                        elif counter == 10:
                            shape = "left"
                        else:
                            shape = "full"
                    else:
                        if counter == 0:
                            shape = "left"
                        elif counter == 10:
                            shape = "right"
                        else:
                            shape = "full"

                    self.one_fig.arrow(
                        step_xb[counter],
                        step_yb[counter],
                        step_x[counter]-step_xb[counter],
                        step_y[counter]-step_yb[counter],
                        head_width=average_h * 0.05,
                        head_length=average_h * 0.2,
                        ec="k",
                        fc="k",
                        shape=shape,
                        length_includes_head=True,
                    )

        for q_id in self.system.loads_q.keys():
            el = self.system.element_map[q_id]
            qi = el.q_load[0]
            q = el.q_load[1]

            x1 = el.vertex_1.x
            y1 = el.vertex_1.y
            x2 = el.vertex_2.x
            y2 = el.vertex_2.y

            if max(qi, q) > 0:
                direction = 1
            else:
                direction = -1

            h1 = 0.3 * max_val * abs(qi) / self.max_q
            h2 = 0.3 * max_val * abs(q) / self.max_q

            ai = np.pi / 2 - el.q_angle
            el_angle = el.angle
            __plot_patch(h1, h2, x1, y1, x2, y2, ai, qi, q, direction, el_angle)

            if el.q_perp_load[0] != 0 or el.q_perp_load[1] != 0:
                qi = el.q_perp_load[0]
                q = el.q_perp_load[1]
                ai = el.q_angle
                x1 = el.vertex_1.x + np.sin(ai) * h1 * direction * 0
                y1 = el.vertex_1.y + np.cos(ai) * h1 * direction * 0
                x2 = el.vertex_2.x + np.sin(ai) * h2 * direction * 0
                y2 = el.vertex_2.y + np.cos(ai) * h2 * direction * 0

                if max(qi, q) > 0:
                    direction = 1
                else:
                    direction = -1

                h1 = 0.3 * max_val * abs(qi) / self.max_q
                h2 = 0.3 * max_val * abs(q) / self.max_q

                ai = -el.q_angle
                el_angle = el.angle
                __plot_patch(h1, h2, x1, y1, x2, y2, ai, qi, q, direction, el_angle)

    @staticmethod
    def __arrow_patch_values(Fx, Fz, node, h):
        """
        :param Fx: (float)
        :param Fz: (float)
        :param node: (Node object)
        :param h: (float) Is a scale variable
        :return: Variables for the matplotlib plotter
        """

        F = (Fx ** 2 + Fz ** 2) ** 0.5
        len_x = 1.2*Fx / F * h
        len_y = 1.2*Fz / F * h
        x = node.vertex.x
        y = node.vertex.y

        return x, y, len_x, len_y, F

    def __point_load_patch(self, max_plot_range, verbosity=0):
        """
        :param max_plot_range: max scale of the plot
        """

        for k in self.system.loads_point:
            Fx, Fz = self.system.loads_point[k]
            # Le cambio el signo para que coincida con el criterio de clase
            Fx = -Fx;
            F = (Fx ** 2 + Fz ** 2) ** 0.5
            node = self.system.node_map[k]
            h = 0.1 * max_plot_range * F / self.max_system_point_load

            x, y, len_x, len_y, F = self.__arrow_patch_values(Fx, Fz, node, h)

            self.one_fig.arrow(
                x,
                y,
                len_x,
                len_y,
                head_width=h * 0.15,
                head_length=0.2 * h,
                ec="b",
                fc="orange",
                zorder=11,
            )
            if verbosity == 0:
                self.one_fig.text(x, y, "F=%d" % F, color="k", fontsize=9, zorder=10)

    def __moment_load_patch(self, max_val):

        h = 0.2 * max_val
        for k, v in self.system.loads_moment.items():

            node = self.system.node_map[k]
            # Le doy la vuelta para que el criterio de signos se adapte a lo explicado en clase
            if v < 0:
                self.one_fig.plot(
                    node.vertex.x,
                    -node.vertex.z,
                    marker=r"$\circlearrowleft$",
                    ms=25,
                    color="orange",
                )
            else:
                self.one_fig.plot(
                    node.vertex.x,
                    -node.vertex.z,
                    marker=r"$\circlearrowright$",
                    ms=25,
                    color="orange",
                )
            self.one_fig.text(
                node.vertex.x + h * 0.2,
                -node.vertex.z + h * 0.2,
                "T=%d" % -v,
                color="k",
                fontsize=9,
                zorder=10,
            )

    def plot_structure(
        self,
        figsize,
        verbosity,
        show=False,
        supports=True,
        scale=1,
        offset=(0, 0),
        gridplot=False,
        annotations=True,
        title: str = '',
    ):
        """
        Representar la estructura
        :param show: (boolean) if True, plt.figure will plot.
        :param supports: (boolean) if True, supports are plotted.
        :param annotations: (boolean) if True, structure annotations are plotted. It includes section name.
        :return:
        """
        if not gridplot:
            self.__start_plot(figsize)

        x, y = super().structure()

        max_x = np.max(x)
        min_x = np.min(x)
        max_y = np.max(y)
        min_y = np.min(y)

        center_x = (max_x - min_x) / 2 + min_x + -offset[0]
        center_y = (max_y - min_y) / 2 + min_y + -offset[1]

        max_plot_range = max(max_x - min_x, max_y - min_y)
        ax_range = max_plot_range * scale
        plusxrange = center_x + ax_range
        plusyrange = center_y + ax_range * figsize[1] / figsize[0]
        minxrange = center_x - ax_range
        minyrange = center_y - ax_range * figsize[1] / figsize[0]

        self.one_fig.axis([minxrange, plusxrange, minyrange, plusyrange])
        plt.title(title)

        for el in self.system.element_map.values():
            x_val, y_val = plot_values_element(el)
            self.one_fig.plot(x_val, y_val, color="black", marker="s")

            if verbosity == 0:
                # add node ID to plot
                ax_range = max_plot_range * 0.015
                self.one_fig.text(
                    x_val[0] + ax_range,
                    y_val[0] + ax_range,
                    "%d" % el.node_id1,
                    color="g",
                    fontsize=9,
                    zorder=10,
                )
                self.one_fig.text(
                    x_val[-1] + ax_range,
                    y_val[-1] + ax_range,
                    "%d" % el.node_id2,
                    color="g",
                    fontsize=9,
                    zorder=10,
                )

                # add element ID to plot
                factor = 0.02 * self.max_val_structure
                x_val = (x_val[0] + x_val[-1]) / 2 - np.sin(el.angle) * factor
                y_val = (y_val[0] + y_val[-1]) / 2 + np.cos(el.angle) * factor

                self.one_fig.text(
                    x_val, y_val, str(el.id), color="r", fontsize=9, zorder=10
                )

                # add element annotation to plot
                # TODO: check how this holds with multiple structure scales.
                if annotations:
                    x_val += +np.sin(el.angle) * factor * 2.3
                    y_val += -np.cos(el.angle) * factor * 2.3
                    self.one_fig.text(
                        x_val, y_val, el.section_name, color="b", fontsize=9, zorder=10
                    )

        # add supports
        if supports:
            self.__fixed_support_patch(max_plot_range * scale)
            self.__hinged_support_patch(max_plot_range * scale)
            self.__rotational_support_patch(max_plot_range * scale)
            self.__roll_support_patch(max_plot_range * scale)
            self.__rotating_spring_support_patch(max_plot_range * scale)
            self.__spring_support_patch(max_plot_range * scale)

        if verbosity == 0:
            # add_loads
            self.__q_load_patch(max_plot_range, verbosity)
            self.__point_load_patch(max_plot_range, verbosity)
            self.__moment_load_patch(max_plot_range)

        if show:
            self.plot()
        else:
            return self.fig

    def _add_node_values(self, x_val, y_val, value_1, value_2, digits):
        offset = self.max_val_structure * 0.015

        # add value to plot
        self.one_fig.text(
            x_val[1] - offset,
            y_val[1] + offset,
            "%s" % round(value_1, digits),
            fontsize=9,
            ha="center",
            va="center",
        )
        self.one_fig.text(
            x_val[-2] - offset,
            y_val[-2] + offset,
            "%s" % round(value_2, digits),
            fontsize=9,
            ha="center",
            va="center",
        )

    def _add_element_values(self, x_val, y_val, value, index, digits=2):
        self.one_fig.text(
            x_val[index],
            y_val[index],
            "%s" % round(value, digits),
            fontsize=9,
            ha="center",
            va="center",
        )

    def plot_result(
        self,
        axis_values,
        force_1=None,
        force_2=None,
        digits=2,
        node_results=True,
        fill_polygon=True,
        color=0,
    ):
        if fill_polygon:
            rec = plt.Polygon(
                np.vstack(axis_values).T, color="C{}".format(color), alpha=0.3
            )
            self.one_fig.add_patch(rec)
        # plot force
        x_val = axis_values[0]
        y_val = axis_values[1]

        self.one_fig.plot(x_val, y_val, color="C{}".format(color))

        if node_results:
            self._add_node_values(x_val, y_val, force_1, force_2, digits)

    def plot(self):
        plt.axis('equal')
        plt.show()

    def axial_force(
        self,
        factor=None,
        figsize=None,
        verbosity=0,
        scale=1,
        offset=(0, 0),
        show=True,
        gridplot=False,
    ):
        self.plot_structure(figsize, 1, scale=scale, offset=offset, gridplot=gridplot)
        con = len(self.system.element_map[1].axial_force)

        if factor is None:
            max_force = max(
                map(
                    lambda el: max(
                        abs(el.N_1),
                        abs(el.N_2),
                        abs(((el.all_qn_load[0] + el.all_qn_load[1]) / 16) * el.l ** 2),
                    ),
                    self.system.element_map.values(),
                )
            )
            factor = det_scaling_factor(max_force, self.max_val_structure)

        for el in self.system.element_map.values():
            if (
                math.isclose(el.N_1, 0, rel_tol=1e-5, abs_tol=1e-9)
                and math.isclose(el.N_2, 0, rel_tol=1e-5, abs_tol=1e-9)
                and math.isclose(el.all_qn_load[0], 0, rel_tol=1e-5, abs_tol=1e-9)
                and math.isclose(el.all_qn_load[1], 0, rel_tol=1e-5, abs_tol=1e-9)
            ):
                continue
            else:
                axis_values = plot_values_axial_force(el, factor, con)
                color = 1 if el.N_1 < 0 else 0
                self.plot_result(
                    axis_values,
                    -el.N_1, # Pongo signo menos para que escriba la etiqueta según el criterio de clase
                    -el.N_2, # Pongo signo menos para que escriba la etiqueta según el criterio de clase
                    node_results=not bool(verbosity),
                    color=color,
                )

                point = (el.vertex_2 - el.vertex_1) / 2 + el.vertex_1
                if el.N_1 < 0:
                    point.displace_polar(
                        alpha=el.angle + 0.5 * np.pi,
                        radius=0.5 * el.N_1 * factor,
                        inverse_z_axis=True,
                    )
                    # cambio signos para que se ajuste a nuestro criterio
                    if verbosity == 0:
                        self.one_fig.text(
                            point.x,
                            point.y,
                            "+",
                            ha="center",
                            va="center",
                            fontsize=20,
                            color="b",
                        )
                if el.N_1 > 0:
                    point.displace_polar(
                        alpha=el.angle + 0.5 * np.pi,
                        radius=0.5 * el.N_1 * factor,
                        inverse_z_axis=True,
                    )
                    # cambio signos para que se ajuste a nuestro criterio
                    if verbosity == 0:
                        self.one_fig.text(
                            point.x,
                            point.y,
                            "-",
                            ha="center",
                            va="center",
                            fontsize=20,
                            color="b",
                        )

        if show:
            self.plot()
        else:
            return self.fig

    def bending_moment(
        self,
        factor=None,
        figsize=None,
        verbosity=0,
        scale=1,
        offset=(0, 0),
        show=True,
        gridplot=False,
    ):
        self.plot_structure(figsize, 1, scale=scale, offset=offset, gridplot=gridplot)
        con = len(self.system.element_map[1].bending_moment)
        if factor is None:
            # maximum moment determined by comparing the node's moments and the sagging moments.
            max_moment = max(
                map(
                    lambda el: max(
                        abs(el.node_1.Ty),
                        abs(el.node_2.Ty),
                        abs(((el.all_qp_load[0] + el.all_qp_load[1]) / 16) * el.l ** 2),
                    )
                    if el.type == "general"
                    else 0,
                    self.system.element_map.values(),
                )
            )
            factor = det_scaling_factor(max_moment, self.max_val_structure)

        # determine the axis values
        cont_elem = 1
        for el in self.system.element_map.values():
            if (
                math.isclose(el.node_1.Ty, 0, rel_tol=1e-5, abs_tol=1e-9)
                and math.isclose(el.node_2.Ty, 0, rel_tol=1e-5, abs_tol=1e-9)
                and math.isclose(el.all_qp_load[0], 0, rel_tol=1e-5, abs_tol=1e-9)
                and math.isclose(el.all_qp_load[1], 0, rel_tol=1e-5, abs_tol=1e-9)
            ):
                # If True there is no bending moment, so no need for plotting.
                continue
            axis_values = plot_values_bending_moment(el, factor, con)
            axis_values_orig = plot_values_bending_moment(el, 0.0, con)
            if verbosity == 0:
                node_results = True
            else:
                node_results = False
            self.plot_result(
                axis_values,
                el.node_1.Ty,
                -el.node_2.Ty,
                node_results=node_results,
            )

            if el.all_qp_load:
                m_sag = max(abs(el.bending_moment))
                index = find_nearest(el.bending_moment, m_sag)[1]
                offset = +self.max_val_structure * 0.001

                if m_sag != abs(el.node_1.Ty):
                 if m_sag != abs(el.node_2.Ty):
                  if verbosity == 0:
                    x = axis_values[0][index] + np.sin(-el.angle) * offset
                    y = axis_values[1][index] + np.cos(-el.angle) * offset
                    x_orig = axis_values_orig[0][index]
                    y_orig = axis_values_orig[1][index]
                    self.one_fig.text(x, y, "%s" % round(m_sag, 1), fontsize=8, color="r")
                    print('Local maximum bending moment - Beam: '+str(cont_elem)+' Mmax:'+str(round(m_sag, 1))+'; Position: (x,y) = ('+str(round(x_orig, 3))+','+str(round(y_orig, 3))+')')
                    cont_elem += 1
        if show:
            self.plot()
        else:
            return self.fig

    def shear_force(
        self,
        factor=None,
        figsize=None,
        verbosity=0,
        scale=1,
        offset=(0, 0),
        show=True,
        gridplot=False,
        include_structure=True,
    ):
        if include_structure:
            self.plot_structure(
                figsize, 1, scale=scale, offset=offset, gridplot=gridplot
            )
        if factor is None:
            max_force = max(
                map(
                    lambda el: np.max(np.abs(el.shear_force)),
                    self.system.element_map.values(),
                )
            )
            factor = det_scaling_factor(max_force, self.max_val_structure)

        for el in self.system.element_map.values():
            if (
                math.isclose(el.node_1.Ty, 0, rel_tol=1e-5, abs_tol=1e-9)
                and math.isclose(el.node_2.Ty, 0, rel_tol=1e-5, abs_tol=1e-9)
                and math.isclose(el.all_qp_load[0], 0, rel_tol=1e-5, abs_tol=1e-9)
                and math.isclose(el.all_qp_load[1], 0, rel_tol=1e-5, abs_tol=1e-9)
            ):
                # If True there is no bending moment and no shear, thus no shear force, so no need for plotting.
                continue
            axis_values = plot_values_shear_force(el, factor)
            # Le cambio el signo para que coincida con lo explicado en clase
            shear_1 = el.shear_force[0]
            shear_2 = el.shear_force[-1]
            if abs(shear_1)<1e-9:
                shear_1 = 0.
            if abs(shear_2)<1e-9:
                shear_2 = 0.

            self.plot_result(
                axis_values, shear_1, shear_2, node_results=not bool(verbosity)
            )
        if show:
            self.plot()
        else:
            return self.fig

    def reaction_force(self, figsize, verbosity, scale, offset, show, gridplot=False):
        self.plot_structure(
            figsize, 1, supports=False, scale=scale, offset=offset, gridplot=gridplot
        )

        h = 0.2 * self.max_val_structure
        max_force = max(
            map(
                lambda node: max(abs(node.Fx), abs(node.Fz)),
                self.system.reaction_forces.values(),
            )
        )
        print('Reacciones')
        print('***************************')
        for node in self.system.reaction_forces.values():
            if not math.isclose(node.Fx, 0, rel_tol=1e-5, abs_tol=1e-9):
                # x direction
                scale = abs(node.Fx) / max_force * h
                sol = self.__arrow_patch_values(-node.Fx, 0, node, scale)
                x = sol[0]
                y = sol[1]
                len_x = sol[2]
                len_y = sol[3]
                
                print('*Nodo: ',node.id)
                print('Reacción Fx: ',-np.round(node.Fx*10000.)/10000.)

                self.one_fig.arrow(
                    x,
                    y,
                    len_x,
                    len_y,
                    head_width=h * 0.15,
                    head_length=0.2 * scale,
                    ec="b",
                    fc="orange",
                    zorder=11,
                )

                if verbosity == 0:
                    self.one_fig.text(
                        x+len_x+h * 0.15,
                        y+len_y,
                        "R=%s" % round(-node.Fx, 2),
                        color="k",
                        fontsize=9,
                        zorder=10,
                    )

            if not math.isclose(node.Fz, 0, rel_tol=1e-5, abs_tol=1e-9):
                # z direction
                scale = abs(node.Fz) / max_force * h
                sol = self.__arrow_patch_values(0, node.Fz, node, scale)
                x = sol[0]
                y = sol[1]
                len_x = sol[2]
                len_y = sol[3]
                
                print('*Nodo: ',node.id)
                print('Reacción Fy: ',np.round(node.Fz*10000.)/10000.)

                self.one_fig.arrow(
                    x,
                    y,
                    len_x,
                    len_y,
                    head_width=h * 0.15,
                    head_length=0.2 * scale,
                    ec="b",
                    fc="orange",
                    zorder=11,
                )

                if verbosity == 0:
                    self.one_fig.text(
                        x+len_x,
                        y+len_y-h * 0.15,
                        "R=%s" % round(node.Fz, 2),
                        color="k",
                        fontsize=9,
                        zorder=10,
                    )

            # Le cambio el signo para que coincida con nuestro criterio
            if not math.isclose(node.Ty, 0, rel_tol=1e-5, abs_tol=1e-9):
                """
                '$...$': render the strings using mathtext
                """
                
                print('*Nodo: ',node.id)
                print('Momento Mz: ',-np.round(node.Ty*10000.)/10000.)
                
                if node.Ty < 0:
                    self.one_fig.plot(
                        node.vertex.x,
                        -node.vertex.z,
                        marker=r"$\circlearrowleft$",
                        ms=25,
                        color="orange",
                    )
                if node.Ty > 0:
                    self.one_fig.plot(
                        node.vertex.x,
                        -node.vertex.z,
                        marker=r"$\circlearrowright$",
                        ms=25,
                        color="orange",
                    )

                if verbosity == 0:
                    self.one_fig.text(
                        node.vertex.x + h * 0.2,
                        -node.vertex.z + h * 0.2,
                        "T=%s" % round(-node.Ty, 2),
                        color="k",
                        fontsize=9,
                        zorder=10,
                    )
        if show:
            self.plot()
        else:
            return self.fig
        print('-------------------------------------------')

    def displacements(
        self,
        factor=None,
        figsize=None,
        verbosity=0,
        scale=1,
        offset=(0, 0),
        show=True,
        linear=False,
        gridplot=False,
    ):
        self.plot_structure(figsize, 1, scale=scale, offset=offset, gridplot=gridplot)
        if factor is None:
            # needed to determine the scaling factor
            max_displacement = max(
                map(
                    lambda el: max(
                        abs(el.node_1.ux), abs(el.node_1.uz),abs(el.node_2.ux), abs(el.node_2.uz), el.max_deflection
                    )
                    if el.type == "general"
                    else 0,
                    self.system.element_map.values(),
                )
            )
            if max_displacement == 0:
             xdisp = self.system.system_displacement_vector[0::3]
             ydisp = self.system.system_displacement_vector[1::3]
             zdisp = self.system.system_displacement_vector[2::3]
             max_displacement = max(np.sqrt(xdisp**2+ydisp**2+zdisp**2))
            factor = det_scaling_factor(max_displacement, self.max_val_structure)

        for el in self.system.element_map.values():
            axis_values = plot_values_deflection(el, factor, linear)
            # Pongo 5 digitos para llegar hasta la centésima de milímetro
            self.plot_result(axis_values, node_results=False, fill_polygon=False, digits=4)

            if el.type == "general":
                # index of the max deflection
                x = np.linspace(el.vertex_1.x, el.vertex_2.x, el.deflection.size)
                y = np.linspace(el.vertex_1.y, el.vertex_2.y, el.deflection.size)
                xd, yd = plot_values_deflection(el, 1.0, linear)
                deflection = ((xd - x) ** 2 + (yd - y) ** 2) ** 0.5
                index = np.argmax(np.abs(deflection))

                if verbosity == 1:

                    if index != 0 or index != el.deflection.size:
                        self._add_element_values(
                            axis_values[0],
                            axis_values[1],
                            deflection[index],
                            index,
                            3,
                        )
        if show:
            self.plot()
        else:
            return self.fig

    def results_plot(
        self,
        verbosity: int = 0,
        scale: float = 1,
        figsize: Tuple[float, float] = (16,11),
        offset: Tuple[float, float] = (0, 0),
        show: bool = True,
    ):
        """
        Juntar todos los gráficos en uno

        :param figsize: (tpl)
        :param verbosity: (int)
        :param scale: (flt)
        :param offset: (tpl)
        :param show: (bool)
        :return: Figure or None
        """
        plt.close("all")
        self.fig = plt.figure(figsize=figsize)
        a = 320
        self.one_fig = self.fig.add_subplot(a + 1)
        self.plot_structure(
            figsize, verbosity, show=False, scale=scale, offset=offset, gridplot=True
        )
        self.one_fig.title.set_text("Estructura")
        self.one_fig = self.fig.add_subplot(a + 2)
        self.bending_moment(None, figsize, verbosity, scale, offset, False, True)
        self.one_fig.title.set_text("Momentos flectores")
        self.one_fig = self.fig.add_subplot(a + 3)
        self.shear_force(None, figsize, verbosity, scale, offset, False, True)
        self.one_fig.title.set_text("Cortantes")
        self.one_fig = self.fig.add_subplot(a + 4)
        self.axial_force(None, figsize, verbosity, scale, offset, False, True)
        self.one_fig.title.set_text("Axiles")
        self.one_fig = self.fig.add_subplot(a + 5)
        self.displacements(None, figsize, verbosity, scale, offset, False, False, True)
        self.one_fig.title.set_text("Desplazamientos")
        self.one_fig = self.fig.add_subplot(a + 6)
        self.reaction_force(figsize, verbosity, scale, offset, False, True)
        self.one_fig.title.set_text("Reacciones")
        if show:
            self.plot()
        else:
            return self.fig
