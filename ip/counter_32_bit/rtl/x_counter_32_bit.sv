module x_counter_32_bit(
   input    logic       i_clk, 
   input    logic       i_rst_n, 
   output   logic       o_count_31,
   output   logic       o_count_30,
   output   logic       o_count_29,
   output   logic       o_count_28,
   output   logic       o_count_27,
   output   logic       o_count_26,
   output   logic       o_count_25,
   output   logic       o_count_24,
   output   logic       o_count_23,
   output   logic       o_count_22,
   output   logic       o_count_21,
   output   logic       o_count_20,
   output   logic       o_count_19,
   output   logic       o_count_18,
   output   logic       o_count_17,
   output   logic       o_count_16,
   output   logic       o_count_15,
   output   logic       o_count_14,
   output   logic       o_count_13,
   output   logic       o_count_12,
   output   logic       o_count_11,
   output   logic       o_count_10,
   output   logic       o_count_9,
   output   logic       o_count_8,
   output   logic       o_count_7,
   output   logic       o_count_6,
   output   logic       o_count_5,
   output   logic       o_count_4,
   output   logic       o_count_3,
   output   logic       o_count_2,
   output   logic       o_count_1,
   output   logic       o_count_0
); 
   logic [31:0] count_q;
   logic [31:0] count_d;

   assign count_d = (count_q + 'd1);

   always_ff@(posedge i_clk) begin 
      if(!i_rst_n)   count_q <= 'd0;
      else           count_q <= count_d;
   end 
     
   assign { o_count_31,
            o_count_30,
            o_count_29,
            o_count_28,
            o_count_27,
            o_count_26,
            o_count_25,
            o_count_24,
            o_count_23,
            o_count_22,
            o_count_21,
            o_count_20,
            o_count_19,
            o_count_18,
            o_count_17,
            o_count_16,
            o_count_15,
            o_count_14,
            o_count_13,
            o_count_12,
            o_count_11,
            o_count_10,
            o_count_9,
            o_count_8,
            o_count_7,
            o_count_6,
            o_count_5,
            o_count_4,
            o_count_3,
            o_count_2,
            o_count_1,
            o_count_0 } = count_q;

endmodule
