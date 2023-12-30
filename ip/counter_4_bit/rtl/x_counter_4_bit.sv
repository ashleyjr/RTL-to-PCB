module x_counter_4_bit(
   input    logic       i_clk, 
   input    logic       i_rst_n,
   output   logic       o_count_3,
   output   logic       o_count_2,
   output   logic       o_count_1,
   output   logic       o_count_0
); 
   logic [3:0] count_q;
   logic [3:0] count_d;

   assign count_d = (count_q + 'd1);

   always_ff@(posedge i_clk) begin 
      if(!i_rst_n)   count_q <= 'd0;
      else           count_q <= count_d;
   end 
     
   assign { o_count_3,
            o_count_2,
            o_count_1,
            o_count_0 } = count_q;

endmodule
