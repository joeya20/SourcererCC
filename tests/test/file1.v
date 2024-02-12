module test;

reg clk;
reg dst, src;

modtest test(
  .clk(clk)
);

always_comb begin
  if(1'b1) begin
    dst = src + 1;
  end else begin
    dst = src + 1;
  end


  if(1'b1) begin
    dst = src + 1;
  end
end

endmodule
