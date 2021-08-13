# Design & Optimization of Programmable Motion Profiling & Control With Autonomous UAV Applications

This is my undergraduate thesis on programmable motion profiling algorithm & its integration with several control applications including a quadrotor with open source APIs.

## Abstract

Many of the motion controllers in the industry use non-programmable motion profiles, which are often limited to modeling a trapezoidal profile with a linear acceleration/deceleration phase, or an s-curve profile of jerk, the derivative of acceleration. Higher order derivatives of velocity are rarely explored to achieve a customized smoothness of the motion profile, which is desired in many real-world applications and robotics systems. The lack of programmability and open-source platforms makes the price of customizing control expensive and the design process redundant for different applications. This thesis provides a low-cost, open-source, and programmable solution that generates motion profiles for a wide range of customized precision levels. We first summarize the common assumptions and generic constraints required to create a smooth motion profile. We review existing approaches of velocity profiling to show the challenges in providing programmability, then offer two implementations of the feedforward motion profiling system as our solution. Performance evaluations of the two implementations are done both mathematically and empirically. Then, this thesis offers an overview on how our motion profile methodology can be integrated into a closed-loop control system of any kind with existing open-source PID feedback for some specific applications. We will use a 1D translation rail to illustrate the effectiveness of higher order motion profiling and the quadrotor demo for autonomous flight to show the compatibility and programmability of the algorithm in large complex systems.

## Acknowledgment

I would like to thank Prof. Jinjun Xiong from the IBM-ILLINOIS Center for Cognitive Computing Systems Research (C3SR) for guiding and pushing me with high standards to achieve what I had never imagined possible. I would also like to thank Bryan Banta from Cal Poly Pomona for the collaboration and support.

## File Description
Documentation folder contains spinets of the code for the different profiling algorithms I developed, which is NOT the final version used in implementation, experiments and the thesis. If you are interested in the details of my thesis, please email me at wenjiey2@illinois.edu.
