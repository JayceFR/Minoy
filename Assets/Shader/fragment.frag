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
        f_color = vec4(0.1725, 0.0588, 0.2, 1.0);
    }
    else if (noise_val  > 0.8){
        f_color = vec4(0.4275, 0.502, 0.9804, 1.0);
    }

    vec4 ui_color = texture(ui_tex, uvs);
    if (ui_color.a > 0){
        f_color = ui_color;
    }
}



void main(){
    overlay_frag();
}