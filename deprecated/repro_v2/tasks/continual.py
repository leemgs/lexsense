#!/usr/bin/env python
import argparse, matplotlib.pyplot as plt
def main():
    months=['Jul','Aug','Sep']; no=[0.89,0.80,0.74]; yes=[0.89,0.86,0.88]
    ap=argparse.ArgumentParser(); ap.add_argument('--plot', default=None); args=ap.parse_args()
    if args.plot:
        plt.figure(); plt.plot(months,no,marker='o',label='No Adaptation'); plt.plot(months,yes,marker='s',label='Periodic Re-training'); plt.ylim(0.7,0.92); plt.ylabel('Macro-F1'); plt.legend(); plt.tight_layout(); plt.savefig(args.plot); print('[plot]', args.plot)
    print({'months':months,'no_adapt':no,'with_adapt':yes})
if __name__=='__main__': main()
