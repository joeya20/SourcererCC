begin
    err_en = On;
    if (lc_tx_test_true_strict(lc_en_i)) begin
        state_d = StActive;
    end
end
