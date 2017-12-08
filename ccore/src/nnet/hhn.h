/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/


#pragma once


#include "utils.hpp"


struct hnn_parameters {
public:
    double m_nu       = utils::random::generate_normal_random(0.5, 0.5);     /* Intrinsic noise      */

    double m_gNa      = 120.0 * (1 + 0.02 * m_nu);    /* Maximal conductivity for sodium current     */
    double m_gK       = 36.0 * (1 + 0.02 * m_nu);     /* Maximal conductivity for potassium current  */
    double m_gL       = 0.3 * (1 + 0.02 * m_nu);      /* Maximal conductivity for leakage current    */

    double m_vNa      = 50.0;                         /* Reverse potential of sodium current [mV]    */
    double m_vK       = -77.0;                        /* Reverse potential of potassium current [mV] */
    double m_vL       = -54.4;                        /* Reverse potantial of leakage current [mV]   */
    double m_vRest    = -65.0;                        /* Rest potential [mV].                        */

    double m_Icn1     = 5.0;            /* External current [mV] for central element 1   */
    double m_Icn2     = 30.0;           /* External current [mV] for central element 2   */

    double m_Vsyninh          = -80.0;  /* Synaptic reversal potential [mV] for inhibitory effects   */
    double m_Vsynexc          = 0.0;    /* Synaptic reversal potential [mV] for exciting effects     */
    double m_alfa_inhibitory  = 6.0;    /* Alfa-parameter for alfa-function for inhibitory effect    */
    double m_betta_inhibitory = 0.3;    /* Betta-parameter for alfa-function for inhibitory effect   */

    double m_alfa_excitatory  = 40.0;   /* Alfa-parameter for alfa-function for excitatoty effect    */
    double m_betta_excitatory = 2.0;    /* Betta-parameter for alfa-function for excitatoty effect   */

    double m_w1 = 0.1;                  /* Strength of the synaptic connection from PN to CN1 */
    double m_w2 = 9.0;                  /* Strength of the synaptic connection from CN1 to PN */
    double m_w3 = 5.0;                  /* Strength of the synaptic connection from CN2 to PN */

    double m_deltah     = 650.0;        /* Period of time [ms] when high strength value of synaptic connection exists from CN2 to PN */
    double m_threshold  = -10;          /* Threshold of the membrane potential that should exceeded by oscillator to be considered as an active */
    double m_eps        = 0.16;         /* Affects pulse counter */
};


struct central_element {
public:
    double m_membrane_potential      = 0.0;     /* Membrane potential of cenral neuron (V)                */
    double m_active_cond_sodium      = 0.0;     /* Activation conductance of the sodium channel (m)       */
    double m_inactive_cond_sodium    = 0.0;     /* Inactivaton conductance of the sodium channel (h)      */
    double m_active_cond_potassium   = 0.0;     /* Activaton conductance of the sodium channel (h)        */

    bool m_pulse_generation         = false;            /* Spike generation of central neuron   */
    std::vector<double> m_pulse_generation_time = { };  /* Timestamps of generated pulses       */
};


struct hhn_oscillator {
    double m_membrane_potential       = 0.0;
    double m_active_cond_sodium       = 0.0;
    double m_inactive_cond_sodium     = 0.0;
    double m_active_cond_potassium    = 0.0;
    double m_link_activation_time     = 0.0;
    double m_link_pulse_counter       = 0.0;
    double m_link_deactivation_time   = 0.0;
    double m_link_weight3             = 0.0;

    bool m_pulse_generation                     = false;
    std::vector<double> m_pulse_generation_time = { };

    double m_noise = utils::random::generate_normal_random(0.5, 0.5);
};


class hhn_network {

};