#version 330 

uniform sampler2D tex;
uniform sampler2D ui_tex;
uniform float time;

uniform sampler2D noise_tex1;
uniform int itime;

in vec2 uvs;
out vec4 f_color;

vec2 random2( vec2 p ) {
    return fract(sin(vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3))))*43758.5453);
}

void overlay_frag(){
    f_color = vec4(texture(tex, uvs).rgb ,1.0);
    vec2 px_uvs = vec2(floor(uvs.x * 320) / 320, floor(uvs.y * 210) / 210);
    float center_dis = distance(uvs, vec2(0.5,0.5));
    float noise_val = center_dis + texture(noise_tex1, vec2(px_uvs.x * 1.52 * 2 + itime * 0.001, px_uvs.y * 2 - itime * 0.002)).r * 0.5;
    vec4 dark = vec4(0.0, 0.0, 0.0, 1.0);
    dark = vec4(0.1176, 0.1137, 0.2235, 1.0);
    float darkness = max(0, noise_val - 0.7) * 10;
    float vignette = max(0, center_dis * center_dis - 0.1) * 5;
    darkness += center_dis;
    f_color = darkness * dark + (1 - darkness) * f_color;

    if ( noise_val > 0.85){
        f_color = vec4(0.3804, 0.2784, 0.8471, 1.0);
    }
    else if (noise_val  > 0.8){
        f_color = vec4(0.4275, 0.502, 0.9804, 1.0);
    }

    vec4 ui_color = texture(ui_tex, uvs);
    if (ui_color.a > 0){
        f_color = ui_color;
    }
}

void slime_frag(){
    vec3 color = vec3(0.2,0.12,0.4);
    vec2 st = uvs;
    st *= 5.0;
    vec2 i_st = floor(st);
    vec2 f_st = fract(st);
    float m_dist = 1.0;  // minimum distance
    for (int j= -1; j <= 1; j++ ) {
        for (int i= -1; i <= 1; i++ ) {
            // Neighbor place in the grid
            vec2 neighbor = vec2(float(i),float(j));

            
            vec2 offset = random2(i_st + neighbor);
            offset = 0.5 + 0.5*sin(time + 6.2831*offset);

            // Position of the cell
            vec2 pos = neighbor + offset - f_st;

            // Cell distance
            float dist = length(pos);

            // Metaball it!
            m_dist = min(m_dist, m_dist*dist);
        }
    }
    color -= step(0.060, m_dist);
    f_color = vec4(color, 1.0);
    vec4 display_color = texture(tex, uvs);
    if (display_color.x > 0){
        f_color = display_color;
    }
    vec4 ui_color = texture(ui_tex, uvs);
    if (ui_color.a > 0){
        f_color = ui_color;
    }  
}

void main(){
    overlay_frag();
}