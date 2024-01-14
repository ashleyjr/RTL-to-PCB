module x_mux_8_to_1(
   input    logic       i_a,
   input    logic       i_b,
   input    logic       i_c,
   input    logic       i_d,
   input    logic       i_e,
   input    logic       i_f,
   input    logic       i_g,
   input    logic       i_h,
   input    logic       i_idx_2,
   input    logic       i_idx_1,
   input    logic       i_idx_0,
   output   logic       o_y
);

   logic [7:0] ins;
   logic [2:0] sel;

   assign sel = { i_idx_2, 
                  i_idx_1, 
                  i_idx_0};

   assign ins = { i_h,
                  i_g,            
                  i_f,
                  i_e,
                  i_d,
                  i_c,
                  i_b,
                  i_a };

   assign o_y = ins[sel];
   
endmodule
