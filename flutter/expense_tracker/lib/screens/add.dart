import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AddExpense extends StatefulWidget {
  const AddExpense({super.key});

  @override
  State<AddExpense> createState() => _AddExpenseState();
}

class _AddExpenseState extends State<AddExpense> {

  String Selected = "";

  DateTime ? selectedDate;        // DateTime is a variable like String and Int, (?) means it can be null

  Future<void> pickedDate() async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(2020),
      lastDate: DateTime(2030),

        builder: (context, child) {
          return Theme(
            data: Theme.of(context).copyWith(
              colorScheme: const ColorScheme.light(
                primary: Color(0XFF1D4ED8),   // selected date
                onPrimary: Colors.white,   // text on selected date
                onSurface: Colors.black,  // normal text
              ),
            ),


            child: child!,
          );
      }


          );

    if (picked != null) {
      setState(() {
        selectedDate = picked;
      });
    }
  }


  @override
  Widget build(BuildContext context) {
    final ScreenWidth = MediaQuery.of(context).size.width;
    final ScreenHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: true,
        centerTitle: true,
        title: Text("Add Expense",
            style: GoogleFonts.poppins(
              fontWeight: FontWeight.bold,
              fontSize: 18
            ),),
      ),
      
      body: SafeArea(
          child: Padding(padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.05),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text("Amount",
              style: TextStyle(
                fontWeight: FontWeight.bold,
              ),
              ),

              SizedBox(height: ScreenHeight * 0.02),

              Padding(padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0),
                child: Container(
                    decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(10),
                        color: Colors.white.withValues(alpha: 0.5),
                        border: Border.all(
                          color: Colors.black.withValues(alpha: 0.1),
                          width: 1.10,
                        )
                    ),

                    child:  TextField(
                      obscureText: false,
                      cursorColor: Colors.grey,
                      decoration: InputDecoration(
                        prefixIcon: Icon(Icons.currency_rupee_rounded, size: 20, color: Colors.black),
                        hintText: "0.00",
                        hintStyle: TextStyle(
                          color: Colors.black54
                        ),
                        enabledBorder: InputBorder.none,
                        focusedBorder: InputBorder.none,
                        prefixIconConstraints: const BoxConstraints(
                          minWidth: 40,
                          minHeight: 40,
                        ),

                      ),
                    )
                ),),

              SizedBox(height: ScreenHeight * 0.03),

              Text("Category",
              style: TextStyle(
                fontWeight: FontWeight.bold,
              ),),

              SizedBox(height: ScreenHeight * 0.02),

              Center(

                child:

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [


                          Expanded(child:       // Mechanism of Expanded:  Available Row Width = 400 px :  Food gets 200 px  : Transport gets 200 px
                                                // Note it cannot control height


                      GestureDetector(
                        onTap: () {
                          setState(() {
                            if (Selected == "Food") {
                              Selected = "";
                              print(Selected);
                            } else {
                              Selected = "Food";
                              print(Selected);
                            }
                          });
                        },

                        child:
                      Container(
                        padding: EdgeInsets.symmetric(vertical: ScreenHeight * 0.02, horizontal: ScreenWidth * 0.07),


                        decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.5),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(
                            color:  Colors.black.withValues(alpha: 0.1),

                          ),
                          boxShadow: Selected == "Food"
                              ? [
                            BoxShadow(
                              color: const Color(0XFF1D4ED8).withValues(alpha: 0.3),
                              blurRadius: 5,
                            ),
                          ]
                              : [],
                        ),
                        child: Column(
                            children: [

                              Icon(Icons.fastfood_rounded, fontWeight: FontWeight.bold, size: 35, color: Colors.orange),

                              SizedBox(height: ScreenHeight * 0.01),

                              Text("Food",
                                style: TextStyle(
                                    color: Colors.black, fontWeight: FontWeight.bold, fontSize: 12
                                ),)
                            ]
                        ),
                      ),
                    ),
                    ),

                          SizedBox(width: ScreenWidth * 0.02),




                          Expanded(child:



                      GestureDetector(
                        onTap: () {
                          setState(() {
                            if (Selected == "Transport") {
                              Selected = "";
                            } else {
                              Selected = "Transport";
                            }
                          });
                        },

                        child:
                        Container(
                          padding: EdgeInsets.symmetric(vertical: ScreenHeight * 0.02, horizontal: ScreenWidth * 0.07),


                          decoration: BoxDecoration(
                            color: Colors.white.withValues(alpha: 0.5),
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(
                             color:  Colors.black.withValues(alpha: 0.1),

                            ),
                            boxShadow: Selected == "Transport"
                                ? [
                              BoxShadow(
                                color: const Color(0XFF1D4ED8).withValues(alpha: 0.3),
                                blurRadius: 5,
                              ),
                            ]
                                : [],
                          ),

                        child: Column(
                            children: [

                              Icon(Icons.directions_bus_rounded, fontWeight: FontWeight.bold, size: 35, color: Colors.blue),

                              SizedBox(height: ScreenHeight * 0.01),

                              Text("Transport",
                                style: GoogleFonts.poppins(
                                    color: Colors.grey, fontWeight: FontWeight.bold, fontSize: ScreenWidth * 0.026
                                ),)
                            ]
                        ),
                      ),
                    ),
                    ),

                    SizedBox(width: ScreenWidth * 0.02),


        Expanded(child:



        GestureDetector(
          onTap: () {
            setState(() {
              if (Selected == "College") {
                Selected = "";
              } else {
                Selected = "College";
              }
            });
          },
          child:
          Container(
            padding: EdgeInsets.symmetric(vertical: ScreenHeight * 0.02, horizontal: ScreenWidth * 0.07),


            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.5),
              borderRadius: BorderRadius.circular(10),
              border: Border.all(
                color:  Colors.black.withValues(alpha: 0.1),

              ),
              boxShadow: Selected == "College"
                  ? [
                BoxShadow(
                  color: const Color(0XFF1D4ED8).withValues(alpha: 0.3),
                  blurRadius: 5,
                ),
              ]
                  : [],
            ),
                        child: Column(
                            children: [

                              Icon(Icons.school_rounded, fontWeight: FontWeight.bold, size: 35, color: Colors.purpleAccent),

                              SizedBox(height: ScreenHeight * 0.01),

                              Text("College",
                                style: TextStyle(
                                    color: Colors.black, fontWeight: FontWeight.bold, fontSize: 12
                                ),)
                            ]
                        ),
                      ),
                    ),
        ),

                  ],
                ),
              ),

              SizedBox(height: ScreenHeight * 0.01),

              Center(

                child:

                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [


                    Expanded(child:       // Mechanism of Expanded:  Available Row Width = 400 px :  Food gets 200 px  : Transport gets 200 px
                    // Note it cannot control height


                    GestureDetector(
                      onTap: () {
                        setState(() {
                          if (Selected == "Entertainment") {
                            Selected = "";
                            print(Selected);
                          } else {
                            Selected = "Entertainment";
                            print(Selected);
                          }
                        });
                      },

                      child:
                      Container(
                        padding: EdgeInsets.symmetric(vertical: ScreenHeight * 0.02, horizontal: ScreenWidth * 0.07),


                        decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.5),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(
                            color:  Colors.black.withValues(alpha: 0.1),

                          ),
                          boxShadow: Selected == "Entertainment"
                              ? [
                            BoxShadow(
                              color: const Color(0XFF1D4ED8).withValues(alpha: 0.3),
                              blurRadius: 5,
                            ),
                          ]
                              : [],
                        ),
                        child: Column(
                            children: [

                              Icon(Icons.sports_esports, fontWeight: FontWeight.bold, size: 35),

                              SizedBox(height: ScreenHeight * 0.01),

                              Text("Entertain",
                                style: TextStyle(
                                    color: Colors.black, fontWeight: FontWeight.bold, fontSize: 12
                                ),)
                            ]
                        ),
                      ),
                    ),
                    ),

                    SizedBox(width: ScreenWidth * 0.02),




                    Expanded(child:



                    GestureDetector(
                      onTap: () {
                        setState(() {
                          if (Selected == "Other") {
                            Selected = "";
                          } else {
                            Selected = "Other";
                          }
                        });
                      },

                      child:
                      Container(
                        padding: EdgeInsets.symmetric(vertical: ScreenHeight * 0.02, horizontal: ScreenWidth * 0.07),


                        decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.5),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(
                            color:  Colors.black.withValues(alpha: 0.1),

                          ),
                          boxShadow: Selected == "Other"
                              ? [
                            BoxShadow(
                              color: const Color(0XFF1D4ED8).withValues(alpha: 0.3),
                              blurRadius: 5,
                            ),
                          ]
                              : [],
                        ),

                        child: Column(
                            children: [

                              Icon(Icons.category_outlined, fontWeight: FontWeight.bold, size: 35, color: Colors.grey),

                              SizedBox(height: ScreenHeight * 0.01),

                              Text("Other",
                                style: TextStyle(
                                    color: Colors.black, fontWeight: FontWeight.bold, fontSize: 12
                                ),)
                            ]
                        ),
                      ),
                    ),
                    ),

                    SizedBox(width: ScreenWidth * 0.02),


                    Expanded(child:

                        SizedBox(width: ScreenWidth  * 0.02)

                    ),

                  ],
                ),
              ),

              SizedBox(height: ScreenHeight * 0.03),


              Text("Date",
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),



              SizedBox(height: ScreenHeight * 0.02),


              GestureDetector(
                onTap: pickedDate,
                child: Container(
                  padding: EdgeInsets.symmetric( horizontal: ScreenWidth * 0.03, vertical: ScreenHeight * 0.02
                  ),
                  decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(10),
                      color: Colors.white.withValues(alpha: 0.5),
                      border: Border.all(
                        color: Colors.black.withValues(alpha: 0.1),
                        width: 1.10,
                      )
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        selectedDate == null
                            ? "Select Date"
                            : "${selectedDate!.day}/${selectedDate!.month}/${selectedDate!.year}",
                      ),
                      const Icon(Icons.calendar_month),
                    ],
                  ),
                ),
              ),

              SizedBox(height: ScreenHeight * 0.05),

              Center(

              child:

              ElevatedButton(
                onPressed: () {

                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Color(0XFF1D4ED8),
                  foregroundColor: Colors.white ,
                  padding: EdgeInsets.symmetric(horizontal: 30, vertical: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),

                child: Padding(padding: EdgeInsets.symmetric(horizontal: ScreenWidth * 0.26),
                  child: Text("Save Expenses",
                    style: GoogleFonts.poppins(
                      fontWeight: FontWeight.bold,
                      fontSize: ScreenWidth * 0.03,
                    ),),
                ),
              ),
              ),
              



            ],
          )
          ),
      ),
    );
  }
}
