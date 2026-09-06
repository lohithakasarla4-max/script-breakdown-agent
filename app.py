import streamlit as st
import json

from agent import analyze_script


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Automated Script & Storyboard Breakdown Agent",
    page_icon="🎬",
    layout="wide"
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🎬 Automated Script & Storyboard Breakdown Agent")

st.write(
    """
    Transform a screenplay into structured production information,
    camera shots, storyboard panels, characters, props, locations,
    costumes, sound effects and continuity notes.
    """
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("🎥 About the Agent")

    st.write(
        """
        This AI agent analyzes screenplay scenes and automatically
        generates a production and storyboard breakdown.
        """
    )

    st.divider()

    st.subheader("The agent identifies:")

    st.write("🎭 Characters")
    st.write("📍 Locations")
    st.write("🎬 Camera shots")
    st.write("🖼️ Storyboard panels")
    st.write("🎒 Props")
    st.write("👗 Costumes")
    st.write("🚗 Vehicles")
    st.write("🔊 Sound effects")
    st.write("🎵 Music")
    st.write("🔄 Continuity")
    st.write("🎥 Production requirements")


# ---------------------------------------------------------
# INPUT
# ---------------------------------------------------------

st.subheader("📝 Enter Screenplay")

script_text = st.text_area(
    "Paste your screenplay below:",
    height=350,
    placeholder="""Example:

INT. COFFEE SHOP - NIGHT

Rain hits the windows.

ARJUN, 22, sits alone at a table.
He looks at his phone.

ARJUN
Where are you?

The door opens.

MEERA enters, carrying a black umbrella.
Arjun looks up.

MEERA
Sorry I'm late.

ARJUN
I thought you weren't coming.

Meera sits across from him.

MEERA
We need to talk.
"""
)


# ---------------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------------

if st.button(
    "🎬 Analyze Screenplay",
    type="primary",
    use_container_width=True
):

    if not script_text.strip():

        st.warning("Please enter a screenplay first.")

    else:

        with st.spinner(
            "🎥 AI is analyzing your screenplay..."
        ):

            result = analyze_script(script_text)

        # -------------------------------------------------
        # ERROR HANDLING
        # -------------------------------------------------

        if "error" in result:

            st.error("Analysis failed.")

            st.code(
                result.get(
                    "details",
                    "Unknown error"
                )
            )

        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        else:

            st.success(
                "✅ Screenplay analysis completed!"
            )


            # -------------------------------------------------
            # PROJECT SUMMARY
            # -------------------------------------------------

            st.header("📚 Project Summary")

            total_scenes = result.get(
                "total_scenes",
                len(result.get("scenes", []))
            )

            st.metric(
                "Total Scenes",
                total_scenes
            )


            # -------------------------------------------------
            # PRODUCTION SUMMARY
            # -------------------------------------------------

            st.header("🎥 Production Summary")

            production = result.get(
                "production_summary",
                {}
            )

            col1, col2, col3 = st.columns(3)

            # ---------------------------------------------
            # LOCATIONS
            # ---------------------------------------------

            with col1:

                st.subheader("📍 Locations")

                locations = production.get(
                    "locations",
                    []
                )

                if locations:

                    for item in locations:
                        st.write(f"• {item}")

                else:
                    st.write("No locations identified.")


            # ---------------------------------------------
            # CHARACTERS
            # ---------------------------------------------

            with col2:

                st.subheader("🎭 Characters")

                characters = production.get(
                    "characters",
                    []
                )

                if characters:

                    for item in characters:
                        st.write(f"• {item}")

                else:
                    st.write("No characters identified.")


            # ---------------------------------------------
            # PROPS
            # ---------------------------------------------

            with col3:

                st.subheader("🎒 Props")

                props = production.get(
                    "props",
                    []
                )

                if props:

                    for item in props:
                        st.write(f"• {item}")

                else:
                    st.write("No props identified.")


            # -------------------------------------------------
            # EXTRA PRODUCTION INFORMATION
            # -------------------------------------------------

            col1, col2, col3 = st.columns(3)

            # ---------------------------------------------
            # VEHICLES
            # ---------------------------------------------

            with col1:

                st.subheader("🚗 Vehicles")

                vehicles = production.get(
                    "vehicles",
                    []
                )

                if vehicles:

                    for item in vehicles:
                        st.write(f"• {item}")

                else:
                    st.write("No vehicles identified.")


            # ---------------------------------------------
            # COSTUMES
            # ---------------------------------------------

            with col2:

                st.subheader("👗 Costumes")

                costumes = production.get(
                    "costumes",
                    []
                )

                if costumes:

                    for item in costumes:
                        st.write(f"• {item}")

                else:
                    st.write("No costume requirements identified.")


            # ---------------------------------------------
            # SPECIAL REQUIREMENTS
            # ---------------------------------------------

            with col3:

                st.subheader("🎬 Special Requirements")

                special_requirements = production.get(
                    "special_requirements",
                    []
                )

                if special_requirements:

                    for item in special_requirements:
                        st.write(f"• {item}")

                else:
                    st.write("No special requirements identified.")


            # -------------------------------------------------
            # SCENE BREAKDOWN
            # -------------------------------------------------

            st.header("🎬 Scene Breakdown")

            scenes = result.get(
                "scenes",
                []
            )

            for scene in scenes:

                scene_number = scene.get(
                    "scene_number",
                    "?"
                )

                heading = scene.get(
                    "scene_heading",
                    "Scene"
                )

                with st.expander(
                    f"Scene {scene_number}: {heading}",
                    expanded=False
                ):

                    # -----------------------------------------
                    # SCENE INFORMATION
                    # -----------------------------------------

                    st.subheader("📍 Scene Information")

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.write(
                            "**Location:**"
                        )

                        st.write(
                            scene.get(
                                "location",
                                "Not identified"
                            )
                        )

                    with col2:

                        st.write(
                            "**Type:**"
                        )

                        st.write(
                            scene.get(
                                "interior_exterior",
                                "Not identified"
                            )
                        )

                    with col3:

                        st.write(
                            "**Time:**"
                        )

                        st.write(
                            scene.get(
                                "time_of_day",
                                "Not identified"
                            )
                        )


                    # -----------------------------------------
                    # CHARACTERS
                    # -----------------------------------------

                    st.subheader("🎭 Characters")

                    characters = scene.get(
                        "characters",
                        []
                    )

                    if characters:

                        for character in characters:
                            st.write(
                                f"• {character}"
                            )

                    else:
                        st.write(
                            "No characters identified."
                        )


                    # -----------------------------------------
                    # ACTION
                    # -----------------------------------------

                    st.subheader("🎞️ Action")

                    st.write(
                        scene.get(
                            "action_summary",
                            "No action summary available."
                        )
                    )


                    # -----------------------------------------
                    # DIALOGUE
                    # -----------------------------------------

                    st.subheader("💬 Dialogue")

                    st.write(
                        scene.get(
                            "dialogue_summary",
                            "No dialogue summary available."
                        )
                    )


                    # -----------------------------------------
                    # PROPS
                    # -----------------------------------------

                    st.subheader("🎒 Props")

                    props = scene.get(
                        "props",
                        []
                    )

                    if props:

                        for prop in props:
                            st.write(
                                f"• {prop}"
                            )

                    else:
                        st.write(
                            "No props identified."
                        )


                    # -----------------------------------------
                    # COSTUMES
                    # -----------------------------------------

                    st.subheader("👗 Costumes")

                    costumes = scene.get(
                        "costume_notes",
                        []
                    )

                    if costumes:

                        for costume in costumes:
                            st.write(
                                f"• {costume}"
                            )

                    else:
                        st.write(
                            "No costume notes identified."
                        )


                    # -----------------------------------------
                    # VEHICLES
                    # -----------------------------------------

                    st.subheader("🚗 Vehicles")

                    vehicles = scene.get(
                        "vehicles",
                        []
                    )

                    if vehicles:

                        for vehicle in vehicles:
                            st.write(
                                f"• {vehicle}"
                            )

                    else:
                        st.write(
                            "No vehicles identified."
                        )


                    # -----------------------------------------
                    # SOUND EFFECTS
                    # -----------------------------------------

                    st.subheader("🔊 Sound Effects")

                    sounds = scene.get(
                        "sound_effects",
                        []
                    )

                    if sounds:

                        for sound in sounds:
                            st.write(
                                f"• {sound}"
                            )

                    else:
                        st.write(
                            "No sound effects identified."
                        )


                    # -----------------------------------------
                    # MUSIC
                    # -----------------------------------------

                    st.subheader("🎵 Music")

                    music = scene.get(
                        "music",
                        []
                    )

                    if music:

                        for track in music:
                            st.write(
                                f"• {track}"
                            )

                    else:
                        st.write(
                            "No music requirements identified."
                        )


                    # -----------------------------------------
                    # VISUAL STYLE
                    # -----------------------------------------

                    st.subheader("🎨 Visual Style")

                    st.write(
                        scene.get(
                            "visual_style",
                            "No visual style specified."
                        )
                    )


                    # -----------------------------------------
                    # CAMERA SHOTS
                    # -----------------------------------------

                    st.subheader("📷 Camera Shots")

                    camera_shots = scene.get(
                        "camera_shots",
                        []
                    )

                    if camera_shots:

                        for shot in camera_shots:

                            st.markdown(
                                f"""
                                **{shot.get("shot", "Shot")}**

                                - **Description:** {shot.get("description", "")}
                                - **Camera Movement:** {shot.get("camera_movement", "")}
                                - **Angle:** {shot.get("angle", "")}
                                """
                            )

                    else:

                        st.write(
                            "No camera shots identified."
                        )


                    # -----------------------------------------
                    # STORYBOARD
                    # -----------------------------------------

                    st.subheader("🖼️ Storyboard")

                    storyboard = scene.get(
                        "storyboard",
                        []
                    )

                    if storyboard:

                        for panel in storyboard:

                            st.markdown(
                                f"""
                                ### Panel {panel.get("panel", "")}

                                **Shot Type:**  
                                {panel.get("shot_type", "")}

                                **Visual Description:**  
                                {panel.get("visual_description", "")}

                                **Characters Visible:**  
                                {", ".join(panel.get("characters_visible", []))}

                                **Action:**  
                                {panel.get("action", "")}

                                **Dialogue:**  
                                {panel.get("dialogue", "")}

                                **Camera:**  
                                {panel.get("camera", "")}
                                """
                            )

                            st.divider()

                    else:

                        st.write(
                            "No storyboard panels generated."
                        )


                    # -----------------------------------------
                    # PRODUCTION REQUIREMENTS
                    # -----------------------------------------

                    st.subheader("🎥 Production Requirements")

                    requirements = scene.get(
                        "production_requirements",
                        []
                    )

                    if requirements:

                        for requirement in requirements:
                            st.write(
                                f"• {requirement}"
                            )

                    else:
                        st.write(
                            "No special production requirements."
                        )


                    # -----------------------------------------
                    # CONTINUITY
                    # -----------------------------------------

                    st.subheader("🔄 Continuity Notes")

                    continuity = scene.get(
                        "continuity_notes",
                        []
                    )

                    if continuity:

                        for note in continuity:
                            st.write(
                                f"• {note}"
                            )

                    else:
                        st.write(
                            "No continuity notes identified."
                        )


            # -------------------------------------------------
            # EXPORT
            # -------------------------------------------------

            st.header("📥 Export")

            json_data = json.dumps(
                result,
                indent=4,
                ensure_ascii=False
            )

            st.download_button(
                label="⬇️ Download Complete Breakdown (JSON)",
                data=json_data,
                file_name="script_breakdown.json",
                mime="application/json",
                use_container_width=True
            )