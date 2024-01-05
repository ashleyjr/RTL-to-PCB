module x_mux_4_to_1(
   input    logic       i_a,
   input    logic       i_b,
   input    logic       i_c,
   input    logic       i_d,
   input    logic       i_idx_1,
   input    logic       i_idx_0,
   output   logic       o_y
);

   logic [3:0] ins;
   logic [1:0] sel;

   assign sel = { i_idx_1, 
                  i_idx_0};

   assign ins = { i_d,
                  i_c,
                  i_b,
                  i_a };

   assign o_y = ins[sel];
   
endmodule
