assign rx_parity_err = rx_valid_q &
                         (^{sreg_q[9:1],parity_odd}); //parity_enable
