import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'add.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {

  int totalSpent = 0;

  int spentToday = 0;
  int spentWeek = 0;
  int spentMonth = 0;
  
  @override
  Widget build(BuildContext context) {
    final ScreenWidth = MediaQuery.of(context).size.width;
    final ScreenHeight = MediaQuery.of(context).size.height;
    return SafeArea(


        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

            SizedBox(height: ScreenHeight * 0.03),

             Padding(padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.05),
                 child: Text("Spend Wisely",
                 style: GoogleFonts.poppins(
                   fontWeight: FontWeight.bold
                 ),)
             ),

            SizedBox(height: ScreenHeight * 0.03),

            Center(
             child: Padding(padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.05),
              child: Container(
                padding: EdgeInsets.all(20),

                width: ScreenWidth ,


                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.5),
                  borderRadius: BorderRadius.circular(10),
                  boxShadow: [
                   BoxShadow(
                     color: Colors.black12,
                     blurRadius: 20
                   )
                  ]
                ),

                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text("Spent This Month",
                    style: GoogleFonts.poppins(
                      color: Colors.black
                    ),),

                    SizedBox(height: ScreenHeight * 0.01),

                    Row(
                      children: [
                        Icon(Icons.currency_rupee_rounded, fontWeight: FontWeight.bold),
                        Text(totalSpent.toString(),
                          style: GoogleFonts.poppins(
                              fontWeight: FontWeight.w600,
                              fontSize: 28
                          ),
                        ),

                        Spacer(),

                        Icon(Icons.wallet_rounded, color: Colors.grey, size: ScreenWidth * 0.15)
                      ],
                    ),


                    SizedBox(height: ScreenHeight * 0.02),


                  Center(
                    child:

                  ElevatedButton(
                    onPressed: () {
                     Navigator.push(context,
                        MaterialPageRoute(builder: (BuildContext context){
                          return AddExpense( );
                        },
                        ),
                      );
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Color(0XFF1D4ED8),
                      foregroundColor: Colors.white ,
                      padding: EdgeInsets.symmetric(horizontal: 30, vertical: 12),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),

                    child: Padding(padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.2),
                      child: Text("+   Add Expense",
                      style: GoogleFonts.poppins(
                        fontWeight: FontWeight.bold,
                        fontSize: ScreenWidth * 0.03,
                      ),),
                  ),
                  ),
                ),

              ]
                ),
              ),
             )
            ),

            SizedBox(height: ScreenHeight * 0.04),

Expanded(child:
        Padding(padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.05),

            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("Expenses by Category",
                  style: GoogleFonts.poppins(
                    fontWeight: FontWeight.bold,
                  ),),

                SizedBox(height: ScreenHeight * 0.02),

            Expanded(child:

            Container(


            width: ScreenWidth ,


            decoration: BoxDecoration(
                color: Colors.white.withValues(alpha: 0.5),
                borderRadius: BorderRadius.circular(10),
                boxShadow: [
                  BoxShadow(
                      color: Colors.black12,
                      blurRadius: 20
                  )
                ]
            ),
            child: Padding(padding: EdgeInsets.symmetric(vertical: ScreenHeight * 0.03),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
              children: [



                Icon(Icons.no_food_outlined, color: Colors.grey, size: 50),

                SizedBox(height: ScreenHeight * 0.02),

                Text("No expenses yet",
                style: GoogleFonts.poppins(
                  fontWeight: FontWeight.bold,
                ),),

                SizedBox(height: ScreenHeight * 0.01),

                Text("Start adding expenses to see",style: GoogleFonts.poppins(color: Colors.black54, fontWeight: FontWeight.bold, fontSize: 12)),

                Text("them here",style: GoogleFonts.poppins(color: Colors.black54, fontWeight: FontWeight.bold, fontSize: 12)),
              ],
              ),
            ),
            ),
            ),



                SizedBox(height: ScreenHeight * 0.03),

                Text("Quick Stats",
                  style: GoogleFonts.poppins(
                    fontWeight: FontWeight.bold,
                  ),),

                SizedBox(height: ScreenHeight * 0.02),








                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [

                    Expanded(child:




            Container(




              decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.5),
                  borderRadius: BorderRadius.circular(10),
                  boxShadow: [
                    BoxShadow(
                        color: Colors.black12,
                        blurRadius: 20
                    )
                  ]
              ),


              child: Padding(padding: EdgeInsets.symmetric(vertical: ScreenHeight * 0.01),
                child: Column(
                children: [


                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.currency_rupee_rounded, fontWeight: FontWeight.bold, size: 17),
                      Text(spentToday.toString(),
                        style: GoogleFonts.poppins(
                            fontWeight: FontWeight.bold,
                            fontSize: 19
                        ),)
                    ],
                  ),

                  Text("Spent Today",
                    style: GoogleFonts.poppins(
                        color: Colors.black54, fontWeight: FontWeight.bold, fontSize: 12
                    ),)
                  ]
              ),
            ),
                    ),
                    ),

                    SizedBox(width: ScreenWidth * 0.02),


                  Expanded(child:


                    Container(


                 //     width: ScreenWidth ,


                      decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.5),
                          borderRadius: BorderRadius.circular(10),
                          boxShadow: [
                            BoxShadow(
                                color: Colors.black12,
                                blurRadius: 20
                            )
                          ]
                      ),
                      child: Padding(padding: EdgeInsets.symmetric(vertical: ScreenHeight * 0.01),
                        child: Column(
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.currency_rupee_rounded, fontWeight: FontWeight.bold, size: 17),
                                Text(spentWeek.toString(),
                                  style: GoogleFonts.poppins(
                                      fontWeight: FontWeight.bold,
                                      fontSize: 19
                                  ),)
                              ],
                            ),

                            Text("This Week",
                              style: GoogleFonts.poppins(
                                  color: Colors.black54, fontWeight: FontWeight.bold, fontSize: 12
                              ),)
                          ]
                      ),
                    ),
                  ),
                  ),

                    SizedBox(width: ScreenWidth * 0.02),


                    Expanded(child:


                      Container(


                            // width: ScreenWidth ,


                        decoration: BoxDecoration(
                            color: Colors.white.withValues(alpha: 0.5),
                            borderRadius: BorderRadius.circular(10),
                            boxShadow: [
                              BoxShadow(
                                  color: Colors.black12,
                                  blurRadius: 20
                              )
                            ]
                        ),
                        child: Padding(padding: EdgeInsets.symmetric(vertical: ScreenHeight * 0.01),
                          child: Column(
                            children: [
                              Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.currency_rupee_rounded, fontWeight: FontWeight.bold, size: 17),
                                  Text(spentMonth.toString(),
                                  style: GoogleFonts.poppins(
                                      fontWeight: FontWeight.bold,
                                      fontSize: 19
                                  ),)
                                ],
                              ),

                              Text("This Month",
                              style: GoogleFonts.poppins(
                                  color: Colors.black54, fontWeight: FontWeight.bold, fontSize: 12
                              ),)
                            ]
                        ),
                      ),
                    ),
                    ),


                      ],

                      ),

                  ],
                ),
                )
),

            SizedBox(height: ScreenHeight * 0.02),


              ],
            ),











        );


  }
}
