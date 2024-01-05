module x_mux_2_to_1(
   input    logic       i_a,
   input    logic       i_b,
   input    logic       i_a_n_b,
   output   logic       o_y
); 

   assign o_y = (i_a_n_b) ? i_a : i_b;
   
endmodule
