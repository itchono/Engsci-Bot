import discord
from discord.ext import commands

import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint
import io

class Biolab(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command()
    async def biolab(self, ctx: commands.Context,
               C_m = 1.0,
               g_Na = 120.0,
               g_K  =  6.0,
               g_L  =   0.3,
               E_Na =  50,
               E_K  = -77.0,
               E_L  = -54.387,
               InjectedCurrent1= 10,
               InjectedCurrent2= 35):
        '''
        Bio lab, with parameters
        C_m  =   1.0
        """membrane capacitance, in uF/cm^2"""

        g_Na = 120.0
        """Sodium (Na) maximum conductances, in mS/cm^2"""

        g_K  =  6.0
        """Postassium (K) maximum conductances, in mS/cm^2"""

        g_L  =   0.3
        """Leak maximum conductances, in mS/cm^2"""

        E_Na =  50
        """Sodium (Na) Nernst reversal potentials, in mV"""

        E_K  = -77.0
        """Postassium (K) Nernst reversal potentials, in mV"""

        E_L  = -54.387
        """Leak Nernst reversal potentials, in mV"""

        t = np.arange(0.0, 450.0, 0.01)
        """ The time to integrate over """

        '''
        t = np.arange(0.0, 450.0, 0.01)


        def alpha_m(V):
            return 0.1*(V+40.0)/(1.0 - np.exp(-(V+40.0) / 10.0))

        def beta_m(V):
            return 4.0*np.exp(-(V+65.0) / 18.0)

        def alpha_h(V):
            return 0.07*np.exp(-(V+65.0) / 20.0)

        def beta_h(V):
            return 1.0/(1.0 + np.exp(-(V+35.0) / 10.0))

        def alpha_n(V):
            return 0.01*(V+55.0)/(1.0 - np.exp(-(V+55.0) / 10.0))

        def beta_n(V):
            return 0.125*np.exp(-(V+65) / 80.0)

        def I_Na(V, m, h):
            return g_Na * m**3 * h * (V - E_Na)

        def I_K(V, n):
            return g_K  * n**4 * (V - E_K)
        #  Leak
        def I_L(V):
            return g_L * (V - E_L)

        def I_inj(t):
            return InjectedCurrent1*(t>100) - InjectedCurrent1*(t>200) + InjectedCurrent2*(t>300) - InjectedCurrent2*(t>400)

        def RHS(X, t):
            V, m, h, n = X

            dVdt = (I_inj(t) - I_Na(V, m, h) - I_K(V, n) - I_L(V)) / C_m
            dmdt = alpha_m(V)*(1.0-m) - beta_m(V)*m
            dhdt = alpha_h(V)*(1.0-h) - beta_h(V)*h
            dndt = alpha_n(V)*(1.0-n) - beta_n(V)*n
            return np.array((dVdt, dmdt, dhdt, dndt))

        X = odeint(RHS, [-65, 0.05, 0.6, 0.32], t)

        V = X[:,0]
        m = X[:,1]
        h = X[:,2]
        n = X[:,3]
        ina = I_Na(V, m, h)
        ik = I_K(V, n)
        il = I_L(V)

        fig = plt.figure()

        plt.subplot(2,1,1)
        plt.title('Hodgkin-Huxley Neuron')
        p1, = plt.plot(t, V, 'k')
        plt.ylabel('V (mV)')

        plt.subplot(2,1,2)
        i_inj_values = [I_inj(t) for t in t]
        p2, = plt.plot(t, i_inj_values, 'k')
        plt.xlabel('t (ms)')
        plt.ylabel('$I_{inj}$ ($\\mu{A}/cm^2$)')
        plt.ylim(-1, 40)
        
        f = io.BytesIO()
        plt.savefig(f, format="png")
        f.seek(0)
        plt.clf()

        await ctx.send(file=discord.File(f, "renderedtex.png"))

