import bpy


class AutoMapBone(bpy.types.Operator):
    bl_idname = 'rebocap.auto_map_bone'
    bl_label = 'Auto Map Bone'

    @classmethod
    def poll(cls, ctx):
        return bpy.data.objects.get(ctx.scene.rebocap_source_armature) != None

    def execute(self, ctx):
        all_names = ('hips', 'spine', 'chest', 'upperChest', 'neck', 'head', 'leftEye', 'rightEye', 'jaw', 'leftUpperLeg', 'leftLowerLeg', 'leftFoot', 'leftToes', 'rightUpperLeg', 'rightLowerLeg', 'rightFoot', 'rightToes', 'leftShoulder', 'leftUpperArm', 'leftLowerArm', 'leftHand', 'rightShoulder', 'rightUpperArm', 'rightLowerArm', 'rightHand', 'leftThumbProximal', 'leftThumbIntermediate', 'leftThumbDistal', 'leftIndexProximal', 'leftIndexIntermediate', 'leftIndexDistal', 'leftMiddleProximal', 'leftMiddleIntermediate', 'leftMiddleDistal', 'leftRingProximal', 'leftRingIntermediate', 'leftRingDistal', 'leftLittleProximal', 'leftLittleIntermediate', 'leftLittleDistal', 'rightThumbProximal', 'rightThumbIntermediate', 'rightThumbDistal', 'rightIndexProximal', 'rightIndexIntermediate', 'rightIndexDistal', 'rightMiddleProximal', 'rightMiddleIntermediate', 'rightMiddleDistal', 'rightRingProximal', 'rightRingIntermediate', 'rightRingDistal', 'rightLittleProximal', 'rightLittleIntermediate', 'rightLittleDistal')
        required_names = ('hips', 'spine', 'chest', 'neck', 'head', 'leftUpperLeg', 'leftLowerLeg', 'leftFoot', 'rightUpperLeg', 'rightLowerLeg', 'rightFoot', 'leftUpperArm', 'leftLowerArm', 'leftHand', 'rightUpperArm', 'rightLowerArm', 'rightHand')
        optional_names = ('upperChest', 'leftEye', 'rightEye', 'jaw', 'leftToes', 'rightToes', 'leftShoulder', 'rightShoulder', 'leftThumbProximal', 'leftThumbIntermediate', 'leftThumbDistal', 'leftIndexProximal', 'leftIndexIntermediate', 'leftIndexDistal', 'leftMiddleProximal', 'leftMiddleIntermediate', 'leftMiddleDistal', 'leftRingProximal', 'leftRingIntermediate', 'leftRingDistal', 'leftLittleProximal', 'leftLittleIntermediate', 'leftLittleDistal', 'rightThumbProximal', 'rightThumbIntermediate', 'rightThumbDistal', 'rightIndexProximal', 'rightIndexIntermediate', 'rightIndexDistal', 'rightMiddleProximal', 'rightMiddleIntermediate', 'rightMiddleDistal', 'rightRingProximal', 'rightRingIntermediate', 'rightRingDistal', 'rightLittleProximal', 'rightLittleIntermediate', 'rightLittleDistal')

        self.bones = [
            "Pelvis", "L_UpLeg", "R_UpLeg", "Spine", "L_DownLeg", "R_DownLeg",
            "Chest", "L_Foot", "R_Foot", "UpChest", "L_Toe", "R_Toe",
            "Neck", "L_Shoulder", "R_Shoulder", "Head", "L_UpArm", "R_UpArm",
            "L_DownArm", "R_DownArm", "L_Palm", "R_Palm", "L_Fingers", "R_Fingers",
        ]
        vrm_bone_list = ['hips', 'leftUpperLeg', 'rightUpperLeg', 'spine', 'leftLowerLeg', 'rightLowerLeg',
                         'chest', 'leftFoot', 'rightFoot', 'upperChest', 'leftToes', 'rightToes',
                         'neck', 'leftShoulder', 'rightShoulder', 'head', 'leftUpperArm', 'rightUpperArm',
                         'leftLowerArm', 'rightLowerArm', 'leftHand', 'rightHand']
        mixamo_bone_list = [
            "mixamorig:Hips", "mixamorig:LeftUpLeg", "mixamorig:RightUpLeg", "mixamorig:Spine", 
            "mixamorig:LeftLeg", "mixamorig:RightLeg", "mixamorig:Spine1", "mixamorig:LeftFoot", 
            "mixamorig:RightFoot", "mixamorig:Spine2", "mixamorig:LeftToeBase", "mixamorig:RightToeBase",
            "mixamorig:Neck", "mixamorig:LeftShoulder", "mixamorig:RightShoulder", "mixamorig:Head", 
            "mixamorig:LeftArm", "mixamorig:RightArm", "mixamorig:LeftForeArm", "mixamorig:RightForeArm",
            "mixamorig:LeftHand", "mixamorig:RightHand"
        ]
        source = bpy.data.objects.get(ctx.scene.rebocap_source_armature)
        if source and source.type == 'ARMATURE':
            armature_data = source.data
            rebocap_bone_map = ctx.scene.rebocap_bone_map
            
            # 1. VRM Detection
            if hasattr(armature_data, 'vrm_addon_extension'):
                mappings = {}
                for human_bone in armature_data.vrm_addon_extension.vrm0.humanoid.human_bones:
                    if human_bone.bone not in all_names:
                        continue
                    if not human_bone.node.bone_name:
                        continue
                    mappings[human_bone.bone] = human_bone.node.bone_name
                
                if mappings:
                    for i in range(22):
                        if vrm_bone_list[i] in mappings:
                            setattr(rebocap_bone_map, f'node_{i}', mappings[vrm_bone_list[i]])
                        else:
                            setattr(rebocap_bone_map, f'node_{i}', '')
                    self.report({'INFO'}, "Detected VRM Armature")
                    return {'FINISHED'}
                    
            # 2. Unreal Engine (UE4/UE5/MetaHuman) Detection
            ue_bone_list = [
                "pelvis", "thigh_l", "thigh_r", "spine_02", "calf_l", "calf_r",
                "spine_04", "foot_l", "foot_r", "spine_05", "ball_l", "ball_r",
                "neck_01", "clavicle_l", "clavicle_r", "head", "upperarm_l", "upperarm_r",
                "lowerarm_l", "lowerarm_r", "hand_l", "hand_r"
            ]
            has_ue = any(b in armature_data.bones for b in ue_bone_list)
            if has_ue:
                for i in range(22):
                    if ue_bone_list[i] in armature_data.bones:
                        setattr(rebocap_bone_map, f'node_{i}', ue_bone_list[i])
                    else:
                        setattr(rebocap_bone_map, f'node_{i}', '')
                self.report({'INFO'}, "Detected Unreal Engine Armature")
                return {'FINISHED'}

            # 3. Rebocap Standard Detection
            rebo_bone_list = [
                "Pelvis", "L_Hip", "R_Hip", "Spine1", "L_Knee", "R_Knee",
                "Spine2", "L_Ankle", "R_Ankle", "Spine3", "L_Foot", "R_Foot",
                "Neck", "L_Collar", "R_Collar", "Head", "L_Shoulder", "R_Shoulder",
                "L_Elbow", "R_Elbow", "L_Wrist", "R_Wrist"
            ]
            has_rebo = any(b in armature_data.bones for b in rebo_bone_list)
            if has_rebo:
                for i in range(22):
                    if rebo_bone_list[i] in armature_data.bones:
                        setattr(rebocap_bone_map, f'node_{i}', rebo_bone_list[i])
                    else:
                        setattr(rebocap_bone_map, f'node_{i}', '')
                self.report({'INFO'}, "Detected Rebocap Standard Armature")
                return {'FINISHED'}

            # 4. Mixamo Detection (with prefix)
            has_mixamo = any(b in armature_data.bones for b in mixamo_bone_list)
            if has_mixamo:
                for i in range(22):
                    if mixamo_bone_list[i] in armature_data.bones:
                        setattr(rebocap_bone_map, f'node_{i}', mixamo_bone_list[i])
                    else:
                        setattr(rebocap_bone_map, f'node_{i}', '')
                self.report({'INFO'}, "Detected Mixamo Armature")
                return {'FINISHED'}
                
            # 5. Mixamo Detection (without prefix)
            mixamo_no_prefix = [name.split(':')[-1] for name in mixamo_bone_list]
            has_mixamo_no_prefix = any(b in armature_data.bones for b in mixamo_no_prefix)
            if has_mixamo_no_prefix:
                for i in range(22):
                    if mixamo_no_prefix[i] in armature_data.bones:
                        setattr(rebocap_bone_map, f'node_{i}', mixamo_no_prefix[i])
                    else:
                        setattr(rebocap_bone_map, f'node_{i}', '')
                self.report({'INFO'}, "Detected Mixamo Armature (No Prefix)")
                return {'FINISHED'}

            self.report({'WARNING'}, "Armature not recognized by any predefined templates")

        return {'FINISHED'}
