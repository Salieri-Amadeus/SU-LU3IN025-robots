def get_team_name():
    return "Splatoon"  # 团队名称

def get_extended_sensors(sensors):
    for key in sensors:
        sensors[key]["distance_to_robot"] = 1.0
        sensors[key]["distance_to_wall"] = 1.0
        if sensors[key]["isRobot"]:
            sensors[key]["distance_to_robot"] = sensors[key]["distance"]
        else:
            sensors[key]["distance_to_wall"] = sensors[key]["distance"]
    return sensors

def step(robotId, sensors):
    sensors = get_extended_sensors(sensors)

    translation = 1  # 默认前进速度
    rotation = 0  # 默认不转向

    # 避免碰撞行为（最高优先级）
    if (sensors["sensor_front_left"]["distance_to_wall"] < 1 and sensors["sensor_front_left"]["distance_to_wall"] > 0.5) or (sensors["sensor_front"]["distance_to_wall"] < 1 and sensors["sensor_front"]["distance_to_wall"] > 0.5):
        rotation = 0.2 + robotId * 0.1  # 向右转
    elif (sensors["sensor_front_right"]["distance_to_wall"] < 1 and sensors["sensor_front_right"]["distance_to_wall"] > 0.5):
        rotation = -0.2 - robotId * 0.1  # 向左转
    elif (sensors["sensor_front_left"]["distance_to_wall"] < 0.5) or (sensors["sensor_front"]["distance_to_wall"] < 0.5):
        rotation = 0.5 + robotId * 0.1
    elif (sensors["sensor_front_right"]["distance_to_wall"] < 0.5):
        rotation = -0.5 - robotId * 0.1
   

    # 避免撞到盟友（次高优先级）
    elif any(sensors[sensor]["isRobot"] and sensors[sensor]["isSameTeam"] for sensor in sensors):
        rotation = 0.2 + robotId * 0.1

    # 追踪敌人（最低优先级）
    elif sensors["sensor_front"]["isRobot"] and not sensors["sensor_front"]["isSameTeam"]:
        rotation = (1) * sensors["sensor_front_left"]["distance_to_robot"] - (1) * sensors["sensor_front_right"]["distance_to_robot"]
    
    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))

    return translation, rotation
