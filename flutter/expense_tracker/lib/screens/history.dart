import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class historyScreen extends StatefulWidget {
  const historyScreen({super.key});

  @override
  State<historyScreen> createState() => _historyScreenState();
}

class _historyScreenState extends State<historyScreen> {

  String selectedFilter = "All";

 
  @override
  Widget build(BuildContext context) {
    final ScreenWidth = MediaQuery.of(context).size.width;
    final ScreenHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      appBar: AppBar(
      title: Text("History",
      style: GoogleFonts.poppins(fontWeight: FontWeight.bold)),
      ),

      body: Column(
        children: [


          SizedBox(height: ScreenHeight * 0.02),

          Center(
              child: Padding(padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.05),
                  child: Container(
                    padding: EdgeInsets.all(8),

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

                    child: Row(
                      children: [
                            GestureDetector(
                              onTap: (){

                                setState(() {
                                if (selectedFilter == "All") {
                                      selectedFilter = "";
                                } else {
                                     selectedFilter = "All";
                                }
                                });
                              },

                              child:
                        Container(
                          padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.025, vertical:  ScreenHeight * 0.01),
                          decoration: BoxDecoration(
                            color: selectedFilter == "All"
                                ? const Color(0XFF1D4ED8)
                                : Colors.transparent,
                            borderRadius: BorderRadius.circular(10),
                          ),

                          child: selectedFilter == "All" ? Text("All", style: GoogleFonts.poppins(color: Colors.white, fontSize: 12)) : Text("All",style: GoogleFonts.poppins( fontSize: 12)),

                        )
                        ),

                        Spacer(),


                        GestureDetector(
                            onTap: (){

                              setState(() {
                                if (selectedFilter == "Today") {
                                  selectedFilter = "";
                                } else {
                                  selectedFilter = "Today";
                                }
                              });
                            },

                            child:
                            Container(
                              padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.025, vertical:  ScreenHeight * 0.01),
                              decoration: BoxDecoration(
                                color: selectedFilter == "Today"
                                    ? const Color(0XFF1D4ED8)
                                    : Colors.transparent,
                                borderRadius: BorderRadius.circular(10),
                              ),

                              child: selectedFilter == "Today" ? Text("Today", style: GoogleFonts.poppins(color: Colors.white, fontSize: 12)) : Text("Today",style: GoogleFonts.poppins( fontSize: 12)),

                            )
                        ),

                        Spacer(),


                        GestureDetector(
                            onTap: (){

                              setState(() {
                                if (selectedFilter == "Yesterday") {
                                  selectedFilter = "";
                                } else {
                                  selectedFilter = "Yesterday";
                                }
                              });
                            },

                            child:
                            Container(
                              padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.025, vertical:  ScreenHeight * 0.01),
                              decoration: BoxDecoration(
                                color: selectedFilter == "Yesterday"
                                    ? const Color(0XFF1D4ED8)
                                    : Colors.transparent,
                                borderRadius: BorderRadius.circular(10),
                              ),

                              child: selectedFilter == "Yesterday" ? Text("Yesterday", style: GoogleFonts.poppins(color: Colors.white, fontSize: 12)) : Text("Yesterday",style: GoogleFonts.poppins( fontSize: 12)),

                            )
                        ),

                        Spacer(),


                        GestureDetector(
                            onTap: (){

                              setState(() {
                                if (selectedFilter == "This Week") {
                                  selectedFilter = "";
                                } else {
                                  selectedFilter = "This Week";
                                }
                              });
                            },

                            child:
                            Container(
                              padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.025, vertical:  ScreenHeight * 0.01),
                              decoration: BoxDecoration(
                                color: selectedFilter == "This Week"
                                    ? const Color(0XFF1D4ED8)
                                    : Colors.transparent,
                                borderRadius: BorderRadius.circular(10),
                              ),

                              child: selectedFilter == "This Week" ? Text("This Week", style: GoogleFonts.poppins(color: Colors.white , fontSize: 12)) : Text("This Week",style: GoogleFonts.poppins( fontSize: 12)),

                            )
                        ),

                        Spacer(),



                        GestureDetector(
                            onTap: (){

                              setState(() {
                                if (selectedFilter == "This Month") {
                                  selectedFilter = "";
                                } else {
                                  selectedFilter = "This Month";
                                }
                              });
                            },

                            child:
                            Container(
                              padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.025, vertical:  ScreenHeight * 0.01),
                              decoration: BoxDecoration(
                                color: selectedFilter == "This Month"
                                    ? const Color(0XFF1D4ED8)
                                    : Colors.transparent,
                                borderRadius: BorderRadius.circular(10),
                              ),

                              child: selectedFilter == "This Month" ? Text("This Month", style: GoogleFonts.poppins(color: Colors.white, fontSize: 12)) : Text("This Month" ,style: GoogleFonts.poppins( fontSize: 12)),

                            )
                        ),
                      ],
                    )
                  ),
              ),
          ),

       
       SizedBox(height: ScreenHeight * 0.25),
          
          Icon(Icons.bookmarks_outlined, size: 60, color: Colors.grey),

          SizedBox(height: ScreenHeight * 0.03),
          
          Text("No expenses yet",style: GoogleFonts.poppins(fontWeight: FontWeight.bold)),
          
          
      ]
      ),
      



    );
  }
}
