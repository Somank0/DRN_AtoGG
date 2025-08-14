import numpy as np
import pickle
import sys
import math
from ROOT import TFile
from ROOT import TLorentzVector
import matplotlib.pyplot as plt
from ROOT import TH1F

"""
Analysis Class:
    Constructor:
        analysis(cut[required: function that provides cuts used],file[optional: name of input file to use], 
                tree[optional: name of tree in file])
    Members:
        mTree(TTree) : Tree read
        inFile(TFile) : input file used
        LeadPhotonP4 : numpy array of TLorentzVector objects of lead photon
        SubLeadPhotonP4 : numpy array of TLorentzVector objects of sublead photon
    Methods:
        plot(outfile[optional]) : Plot histograms off m,pt,eta,y and save in root file
        getValues() : get an array of m,pt,eta,y
        printTree() : print the tree read
"""
###########CLASS DEFINATION########################
class analysis:
    def readTree(self, file, tree):
        try:
            self.inFile = TFile(file)
            self.mTree = self.inFile.Get(tree)
            print("Analysing Category: ", tree)
        except (OSError, FileNotFoundError, IOError):
            print("Error reading file:", file)

    def plot(self, outfile="GGF_NTuple_Analyzed_FOO.root"):
        DiPho_Mass_Hist = TH1F("DiPho_Mass_Hist", "DiPho_Mass_Hist", 200, 0.0, 200.0)
        DiPho_Pt_Hist = TH1F("DiPho_Pt_Hist", "DiPho_Pt_Hist", 100, 0.0, 1000.0)
        DiPho_Eta_Hist = TH1F("DiPho_Eta_Hist", "DiPho_Eta_Hist", 100, -5.0, 5.0)
        DiPho_Y_Hist = TH1F("DiPho_Y_Hist", "DiPho_Y_Hist", 100, -5.0, 5.0)
        for i in self.LeadPhotonP4 + self.SubLeadPhotonP4:
            DiPho_Mass_Hist.Fill(i.M())
            DiPho_Pt_Hist.Fill(i.Pt())
            DiPho_Eta_Hist.Fill(i.Eta())
            DiPho_Y_Hist.Fill(i.Rapidity())
        output = TFile(outfile, "RECREATE")
        output.cd()
        DiPho_Mass_Hist.Write()
        DiPho_Pt_Hist.Write()
        DiPho_Eta_Hist.Write()
        DiPho_Y_Hist.Write()
        output.Close()
        print("Mass,Pt,Eta and Y plots written in file ", outfile)

    def getMass(self):
        return [i.M() for i in (self.LeadPhotonP4 + self.SubLeadPhotonP4)]

    def getValues(self):
        return (
            [i.M() for i in (self.LeadPhotonP4 + self.SubLeadPhotonP4)],
            [i.Pt() for i in (self.LeadPhotonP4 + self.SubLeadPhotonP4)],
            [i.Eta() for i in (self.LeadPhotonP4 + self.SubLeadPhotonP4)],
            [i.Rapidity() for i in (self.LeadPhotonP4 + self.SubLeadPhotonP4)],
        )

    def printTree(self):
        if self.mTree != None:
            self.mTree.Print()

    def getPhotons(self, cuts):
        if self.mTree == None:
            return
        for event in self.mTree:
            LeadPhotonP4 = TLorentzVector()
            SubLeadPhotonP4 = TLorentzVector()
            if cuts(event):
                continue
            LeadPhotonP4.SetPtEtaPhiE(
                (event.Ele_Gen_Pt)[0],
                (event.Ele_Gen_Eta)[0],
                (event.Ele_Gen_Phi)[0],
                (event.Ele_Gen_E)[0],
            )
            self.LeadPhotonP4 = np.append(self.LeadPhotonP4, LeadPhotonP4)
            SubLeadPhotonP4.SetPtEtaPhiE(
                (event.Ele_Gen_Pt)[1],
                (event.Ele_Gen_Eta)[1],
                (event.Ele_Gen_Phi)[1],
                (event.Ele_Gen_E)[1],
            ),
            self.SubLeadPhotonP4 = np.append(self.SubLeadPhotonP4, [SubLeadPhotonP4])

    def __init__(
        self, cuts, file="merged.root", tree="nTuplelize/T"
    ) -> None:
        self.inFile = None
        self.mTree = None
        self.LeadPhotonP4 = np.array([])
        self.SubLeadPhotonP4 = np.array([])
        self.readTree(file, tree)
        self.getPhotons(cuts)

    def __del__(self):
        if self.inFile != None:
            self.inFile.Close()


########END CLASS DEFINATION#########

LeadElectronCut = float(sys.argv[1])  # Supply Lead photon pt cut
SubLeadElectronCut = float(sys.argv[2])  # Supply sublead photon pt cut

# Define cuts in this function
def cuts(event):
    if int(event.Ele_Gen_Pt.size()) < 2:
        return True
    if event.Ele_Gen_Pt[0] < 20 or event.Ele_Gen_Pt[1] < 20:
        return True
    if abs(event.Ele_Gen_Eta[0]) > 1.4442 or abs(event.Ele_Gen_Eta[1]) > 1.4442:
        return True

    if (
        event.Ele_Gen_Pt[0] > LeadElectronCut
        or event.Ele_Gen_Pt[1] > SubLeadElectronCut
    ):
        return True
    #    if math.sqrt(event.Ele_Gen_Eta[0] ** 2 + event.Ele_Gen_Phi[0] ** 2) > 2:
    #        return True
    #    if math.sqrt(event.Ele_Gen_Eta[1] ** 2 + event.Ele_Gen_Phi[1] ** 2) > 2:
    #        return True
    return False


# TODO: Supply an cuts function which takes in event as an argument
print("Cuts used for Pt of LeadPhoton", LeadElectronCut)
print("Cuts used for Pt of SubLeadPhoton", SubLeadElectronCut)
foo = analysis(cuts)
# if foo.mTree != None:
#    for event in foo.mTree:
#        try:
#            dR = np.append(
#                dR,
#                math.log(
#                    math.sqrt(
#                        (event.eta[0] - event.Ele_Gen_Eta[0]) ** 2
#                        + (event.phi[0] - event.Ele_Gen_Phi[0]) ** 2
#                    )
#                ),
#            )
#        except IndexError:
#            pass
# fig, axs = plt.subplots(1, 1, figsize=(10, 7), tight_layout=True)

## Show plot

# axs.hist(dR, bins=100, label="dR")
# plt.savefig("recoe.png")
## Show plot
# plt.show()


mass = np.array(foo.getMass())
with open("trueE_target.pickle", "wb") as outpickle:
    pickle.dump(mass, outpickle)
