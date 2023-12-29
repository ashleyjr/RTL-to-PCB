module x_shift_32_bit(
   input    logic       i_clk, 
   input    logic       i_rst_n,
   input    logic       i_in,
   output   logic       o_out
); 
   logic [31:0] shift_q;
   logic [31:0] shift_d;

   assign shift_d = {shift_q[30:0],i_in};

   always_ff@(posedge i_clk) begin 
      if(!i_rst_n)   shift_q <= 'd0;
      else           shift_q <= shift_d;
   end 
    
   assign o_out = shift_q[31];
   
endmodule
