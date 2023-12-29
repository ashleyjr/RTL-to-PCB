module x_lut_4_bit(
   input    logic       i_clk, 
   input    logic       i_rst_n,
   // Setup chain
   input    logic       i_chain_data,
   input    logic       i_chain_en,
   // Functional
   input    logic       i_in_3,
   input    logic       i_in_2,
   input    logic       i_in_1,
   input    logic       i_in_0,
   output   logic       o_out
); 
   // Configure LUT
   logic [15:0] chain_q;
   logic [15:0] chain_d;

   assign chain_d = (i_chain_en) ? {chain_q[15:0],i_chain_data} : chain_q;

   always_ff@(posedge i_clk) begin 
      if(!i_rst_n)   chain_q <= 'd0;
      else           chain_q <= chain_d;
   end 
   
   // Access LUT
   logic [3:0] sel;

   assign sel = { i_in_3,
                  i_in_2,
                  i_in_1,
                  i_in_0   };

   assign o_out = chain_q[sel];
   
endmodule
