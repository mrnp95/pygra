from . import specialhopping
from . import specialgeometry
import numpy as np
from . import geometry


def tbg(n=7,ti=0.12,lambi=3.0,lamb=3.0,is_sparse=True,
        has_spin=False,dl=3.0):
    """
    Return the Hamiltonian of twisted bilayer graphene
    """
    g = specialgeometry.twisted_bilayer(n,dz=dl/2.0)
    mgenerator = specialhopping.twisted_matrix(ti=ti,
            lambi=lambi,lamb=lamb,dl=dl)
    h = g.get_hamiltonian(is_sparse=is_sparse,has_spin=has_spin,
            is_multicell=True,mgenerator=mgenerator)
    return h


def multilayer_graphene(l=[0],real=False,**kwargs):
  """Return the hamiltonian of multilayer graphene"""
  g = specialgeometry.multilayer_graphene(l=l)
  g.center()
  if real: # real tight binding hopping
      mgenerator = specialhopping.twisted_matrix(**kwargs)
      h = g.get_hamiltonian(has_spin=False,
          mgenerator=mgenerator)
  else:
    h = g.get_hamiltonian(has_spin=False,
          fun=specialhopping.multilayer(**kwargs))
  return h


def flux2d(g,n=1,m=1):
    """Return a Hamiltonian with a certain commensurate flux per unit cell"""
    from pygra import sculpt
    from pygra import supercell
    g = supercell.target_angle(g,0.5) # target a orthogonal cell
    g = sculpt.rotate_a2b(g,g.a1,np.array([1.,0.,0.])) # set in the x direction
    g = g.supercell([1,n,1])
    h = g.get_hamiltonian(has_spin=False)
    r = np.array([0.,1.,0.])
    dr = g.a2.dot(r) # distance
    h.add_peierls(m*2.*np.pi/dr)
    return h



def valence_TMDC(g=None,soc=0.0):
    """Return the Hamiltonian for the valence band of a TMDC"""
    if g is None:
        g = geometry.triangular_lattice()
    ft = specialhopping.phase_C3_matrix(g,phi=soc)
    h = g.get_hamiltonian(mgenerator=ft,is_multicell=True,has_spin=False)
    h.turn_spinful(enforce_tr=True)
    return h # return the Hamiltonian



def NbSe2(soc=0.0):
    """Return the Hamiltonian of NbSe2"""
    g = geometry.triangular_lattice()  # triangular lattice
#    ts = np.array([86.8,139.9,29.6,3.5,3.3])
    ts = np.array([46.,257.5,4.4,-15,6])
    ts = np.array([-0.2,1.,0.,0.,0.])
    t = ts[0]/np.max(ts) # 1NN 
#    ts[0] = 0.0 # set to zero
    ts = ts/np.max(ts) # normalize
    fm = specialhopping.neighbor_hopping_matrix(g,ts) # function for hoppings
    h = g.get_hamiltonian(mgenerator=fm,is_multicell=True,has_spin=True,
            cutoff=len(ts))
    ## Now add the SOC if necessary
    if soc!=0.0:
      hsoc = valence_TMDC(g=h.geometry,soc=soc) # hamiltonian with SOC
      h = h + t*hsoc # add the two Hamiltonians
    h.set_filling(.5)
#    h = h.supercell(4)
#    m = np.array(h.intra.todense()).reshape(h.intra.shape[0]**2)
    return h
    










