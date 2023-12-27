module x_counter_8_bit(
   input    logic       i_clk, 
   input    logic       i_rst_n,
   output   logic       o_count_7,
   output   logic       o_count_6,
   output   logic       o_count_5,
   output   logic       o_count_4,
   output   logic       o_count_3,
   output   logic       o_count_2,
   output   logic       o_count_1,
   output   logic       o_count_0,
); 
   logic [7:0] count_q;
   logic [7:0] count_d;

   assign count_d = (count_q + 'd1);

   always_ff@(posedge i_clk or negedge i_rst_n) begin 
      if(!i_rst_n)   count_q <= 'd0;
      else           count_q <= count_d;
   end 
     
   assign { o_count_7,
            o_count_6,
            o_count_5,
            o_count_4,
            o_count_3,
            o_count_2,
            o_count_1,
            o_count_0 } = count_q;

endmodule
