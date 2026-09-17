function wave_gui
% wave_gui.m
% MATLAB GUI for layered P-SV-SH wave calculation
% Symbol system follows the user's notation:
%   a : upper medium
%   1 : middle layer
%   g : lower medium
% Results displayed in LaTeX style on the right side.

    p0 = defaultParams();

    fig = figure( ...
        'Name', 'P-SV-SH Wave GUI', ...
        'NumberTitle', 'off', ...
        'Color', 'w', ...
        'MenuBar', 'none', ...
        'ToolBar', 'none', ...
        'Units', 'normalized', ...
        'Position', [0.03 0.05 0.94 0.88]);

    try
        fig.WindowState = 'maximized';
    catch
        set(fig, 'OuterPosition', [0 0 1 1]);
    end

    leftPanel = uipanel( ...
        'Parent', fig, ...
        'Title', 'Input Parameters', ...
        'FontWeight', 'bold', ...
        'Units', 'normalized', ...
        'Position', [0.015 0.03 0.28 0.94], ...
        'BackgroundColor', 'w');

    rightPanel = uipanel( ...
        'Parent', fig, ...
        'Title', 'Results', ...
        'FontWeight', 'bold', ...
        'Units', 'normalized', ...
        'Position', [0.31 0.03 0.675 0.94], ...
        'BackgroundColor', 'w');

    tg = uitabgroup( ...
        'Parent', rightPanel, ...
        'Units', 'normalized', ...
        'Position', [0.01 0.01 0.98 0.98]);

    tabDerived = uitab(tg, 'Title', 'Derived');
    tabP       = uitab(tg, 'Title', 'P incidence');
    tabSV      = uitab(tg, 'Title', 'SV incidence');
    tabSH      = uitab(tg, 'Title', 'SH incidence');
    tabEnergy  = uitab(tg, 'Title', 'Energy check');

    axDerived = makeAxes(tabDerived);
    axP       = makeAxes(tabP);
    axSV      = makeAxes(tabSV);
    axSH      = makeAxes(tabSH);
    axEnergy  = makeAxes(tabEnergy);

    fields = struct();

    y = 0.95;
    dy = 0.048;

    addSection(leftPanel, 'Reference scales / general', y); y = y - 0.055;
    fields.omega = addField(leftPanel, '\omega', p0.omega, y); y = y - dy;
    fields.mu_a  = addField(leftPanel, '\mu_a', p0.mu_a, y);   y = y - dy;
    fields.rho_a = addField(leftPanel, '\rho_a', p0.rho_a, y); y = y - dy;
    fields.Phi_i = addField(leftPanel, '\phi_i', p0.Phi_i, y); y = y - dy;
    fields.Psi_i = addField(leftPanel, '\psi_i', p0.Psi_i, y); y = y - dy - 0.01;

    addSection(leftPanel, 'Medium a', y); y = y - 0.055;
    fields.lambda_a = addField(leftPanel, '\lambda_a', p0.lambda_a, y); y = y - dy;
    fields.mu_a2    = addField(leftPanel, '\mu_a',     p0.mu_a,     y); y = y - dy;
    fields.rho_a2   = addField(leftPanel, '\rho_a',    p0.rho_a,    y); y = y - dy - 0.01;

    addSection(leftPanel, 'Layer 1', y); y = y - 0.055;
    fields.lambda_1 = addField(leftPanel, '\lambda_1', p0.lambda_1, y); y = y - dy;
    fields.mu_1     = addField(leftPanel, '\mu_1',     p0.mu_1,     y); y = y - dy;
    fields.rho_1    = addField(leftPanel, '\rho_1',    p0.rho_1,    y); y = y - dy;
    fields.h_1      = addField(leftPanel, 'h_1',       p0.h_1,      y); y = y - dy - 0.01;

    addSection(leftPanel, 'Medium g', y); y = y - 0.055;
    fields.lambda_g = addField(leftPanel, '\lambda_g', p0.lambda_g, y); y = y - dy;
    fields.mu_g     = addField(leftPanel, '\mu_g',     p0.mu_g,     y); y = y - dy;
    fields.rho_g    = addField(leftPanel, '\rho_g',    p0.rho_g,    y); y = y - dy - 0.01;

    addSection(leftPanel, 'Horizontal wavenumber', y); y = y - 0.055;
    fields.k_x      = addField(leftPanel, 'k_x',       p0.k_x,      y); y = y - dy;

    uicontrol( ...
        'Parent', leftPanel, ...
        'Style', 'pushbutton', ...
        'String', 'Compute', ...
        'Units', 'normalized', ...
        'Position', [0.06 0.025 0.26 0.05], ...
        'FontSize', 10.5, ...
        'FontWeight', 'bold', ...
        'Callback', @onCompute);

    uicontrol( ...
        'Parent', leftPanel, ...
        'Style', 'pushbutton', ...
        'String', 'Reset', ...
        'Units', 'normalized', ...
        'Position', [0.37 0.025 0.26 0.05], ...
        'FontSize', 10.5, ...
        'FontWeight', 'bold', ...
        'Callback', @onReset);

    uicontrol( ...
        'Parent', leftPanel, ...
        'Style', 'pushbutton', ...
        'String', 'Load Example 1', ...
        'Units', 'normalized', ...
        'Position', [0.68 0.025 0.26 0.05], ...
        'FontSize', 10.5, ...
        'FontWeight', 'bold', ...
        'Callback', @onLoadExample);

    onLoadExample();

    function ax = makeAxes(parentObj)
        ax = axes( ...
            'Parent', parentObj, ...
            'Units', 'normalized', ...
            'Position', [0.02 0.02 0.96 0.96]);
        axis(ax, [0 1 0 1]);
        axis(ax, 'off');
    end

    function addSection(parentPanel, txt, ypos)
        uicontrol( ...
            'Parent', parentPanel, ...
            'Style', 'text', ...
            'String', txt, ...
            'Units', 'normalized', ...
            'Position', [0.05 ypos 0.90 0.035], ...
            'BackgroundColor', 'w', ...
            'HorizontalAlignment', 'left', ...
            'FontWeight', 'bold', ...
            'FontSize', 10.5);
    end

    function h = addField(parentPanel, labelText, value, ypos)
        uicontrol( ...
            'Parent', parentPanel, ...
            'Style', 'text', ...
            'String', labelText, ...
            'Units', 'normalized', ...
            'Position', [0.06 ypos 0.32 0.034], ...
            'BackgroundColor', 'w', ...
            'HorizontalAlignment', 'left', ...
            'FontSize', 10);

        h = uicontrol( ...
            'Parent', parentPanel, ...
            'Style', 'edit', ...
            'String', num2str(value, '%.10g'), ...
            'Units', 'normalized', ...
            'Position', [0.38 ypos 0.53 0.040], ...
            'BackgroundColor', 'white', ...
            'HorizontalAlignment', 'left', ...
            'FontSize', 10, ...
            'Callback', @onCompute);
    end

    function onLoadExample(~, ~)
        p = defaultParams();
        names = fieldnames(fields);
        for ii = 1:numel(names)
            key = names{ii};
            switch key
                case 'mu_a2'
                    set(fields.(key), 'String', num2str(p.mu_a, '%.10g'));
                case 'rho_a2'
                    set(fields.(key), 'String', num2str(p.rho_a, '%.10g'));
                otherwise
                    set(fields.(key), 'String', num2str(p.(key), '%.10g'));
            end
        end
        onCompute();
    end

    function onReset(~, ~)
        onLoadExample();
    end

    function p = readInputs()
        p = struct();
        p.omega    = readField(fields.omega, 'omega');
        p.mu_a     = readField(fields.mu_a, 'mu_a');
        p.rho_a    = readField(fields.rho_a, 'rho_a');
        p.Phi_i    = readField(fields.Phi_i, 'Phi_i');
        p.Psi_i    = readField(fields.Psi_i, 'Psi_i');

        p.lambda_a = readField(fields.lambda_a, 'lambda_a');
        mu_a_2     = readField(fields.mu_a2, 'mu_a(second)', false);
        rho_a_2    = readField(fields.rho_a2, 'rho_a(second)', false);

        p.lambda_1 = readField(fields.lambda_1, 'lambda_1');
        p.mu_1     = readField(fields.mu_1, 'mu_1');
        p.rho_1    = readField(fields.rho_1, 'rho_1');
        p.h_1      = readField(fields.h_1, 'h_1');

        p.lambda_g = readField(fields.lambda_g, 'lambda_g');
        p.mu_g     = readField(fields.mu_g, 'mu_g');
        p.rho_g    = readField(fields.rho_g, 'rho_g');

        p.k_x      = readField(fields.k_x, 'k_x');

        % keep duplicated a-medium entries consistent
        if abs(mu_a_2 - p.mu_a) > 1e-12 || abs(rho_a_2 - p.rho_a) > 1e-12
            p.mu_a  = mu_a_2;
            p.rho_a = rho_a_2;
            set(fields.mu_a,  'String', num2str(p.mu_a,  '%.10g'));
            set(fields.rho_a, 'String', num2str(p.rho_a, '%.10g'));
        end
    end

    function v = readField(h, name, mustRealPositive)
        if nargin < 3
            mustRealPositive = true;
        end
        v = str2double(get(h, 'String'));
        if isnan(v)
            error('Invalid numeric input: %s', name);
        end
        if mustRealPositive && ~isfinite(v)
            error('Invalid numeric input: %s', name);
        end
    end

    function onCompute(~, ~)
        try
            p = readInputs();
            out = computeModel(p);
            drawDerived(axDerived, p, out);
            drawP(axP, out);
            drawSV(axSV, out);
            drawSH(axSH, out);
            drawEnergy(axEnergy, out);
        catch ME
            drawError(axDerived, ME.message);
            drawError(axP,       ME.message);
            drawError(axSV,      ME.message);
            drawError(axSH,      ME.message);
            drawError(axEnergy,  ME.message);
        end
    end
end

function p = defaultParams()
% Example 1 normalization:
% mu_a = 1, rho_a = 1, omega = 1
% lambda_a = 1.3 mu_a
% mu_1 = 1.5 mu_a, lambda_1 = 4.0 mu_a
% mu_g = 5.2 mu_a, lambda_g = 1.3 mu_a
% rho_1 = 4.4 rho_a, rho_g = 1.9 rho_a
% k_x = 0.1 omega sqrt(rho_a / mu_a)
% h_1 = 9.8 sqrt(mu_a / (omega^2 rho_a))
    p.omega    = 1.0;
    p.mu_a     = 1.0;
    p.rho_a    = 1.0;
    p.lambda_a = 1.3 * p.mu_a;

    p.mu_1     = 1.5 * p.mu_a;
    p.lambda_1 = 4.0 * p.mu_a;
    p.rho_1    = 4.4 * p.rho_a;

    p.mu_g     = 5.2 * p.mu_a;
    p.lambda_g = 1.3 * p.mu_a;
    p.rho_g    = 1.9 * p.rho_a;

    p.k_x      = 0.1 * p.omega * sqrt(p.rho_a / p.mu_a);
    p.h_1      = 9.8 * sqrt(p.mu_a / (p.omega^2 * p.rho_a));

    p.Phi_i    = 1.0;
    p.Psi_i    = 1.0;
end

function out = computeModel(p)
    % ----------- basic wave numbers / angles / speeds -----------
    out.eta_a = p.rho_a;
    out.eta_g = p.rho_g;

    out.kPa = p.omega * sqrt(p.rho_a / (p.lambda_a + 2 * p.mu_a));
    out.kSa = p.omega * sqrt(p.rho_a / p.mu_a);
    out.zeta_a = p.mu_a / (p.lambda_a + 2 * p.mu_a);
    out.thetaPa = asin(p.k_x / out.kPa);
    out.thetaSa = asin(p.k_x / out.kSa);
    out.cPa = 1 / sqrt(p.rho_a / (p.lambda_a + 2 * p.mu_a));
    out.cSa = 1 / sqrt(p.rho_a / p.mu_a);

    out.kP1 = p.omega * sqrt(p.rho_1 / (p.lambda_1 + 2 * p.mu_1));
    out.kS1 = p.omega * sqrt(p.rho_1 / p.mu_1);
    out.zeta_1 = p.mu_1 / (p.lambda_1 + 2 * p.mu_1);
    out.thetaP1 = asin(p.k_x / out.kP1);
    out.thetaS1 = asin(p.k_x / out.kS1);
    out.varphiP1 = out.kP1 * p.h_1 * cos(out.thetaP1);
    out.varphiS1 = out.kS1 * p.h_1 * cos(out.thetaS1);

    out.kPg = p.omega * sqrt(p.rho_g / (p.lambda_g + 2 * p.mu_g));
    out.kSg = p.omega * sqrt(p.rho_g / p.mu_g);
    out.zeta_g = p.mu_g / (p.lambda_g + 2 * p.mu_g);
    out.thetaPg = asin(p.k_x / out.kPg);
    out.thetaSg = asin(p.k_x / out.kSg);
    out.cPg = 1 / sqrt(p.rho_g / (p.lambda_g + 2 * p.mu_g));
    out.cSg = 1 / sqrt(p.rho_g / p.mu_g);

    % ----------- transfer matrix of layer 1 -----------
    A0 = [ ...
        1, 1, -cot(out.thetaS1),  cot(out.thetaS1); ...
        cot(out.thetaP1), -cot(out.thetaP1), 1, 1; ...
        p.rho_1 * out.zeta_1 * sin(2 * out.thetaP1), ...
       -p.rho_1 * out.zeta_1 * sin(2 * out.thetaP1), ...
       -p.rho_1 * cos(2 * out.thetaS1), ...
       -p.rho_1 * cos(2 * out.thetaS1); ...
        p.rho_1 * cos(2 * out.thetaS1), ...
        p.rho_1 * cos(2 * out.thetaS1), ...
        p.rho_1 * sin(2 * out.thetaS1), ...
       -p.rho_1 * sin(2 * out.thetaS1)];

    Aphi = [ ...
        exp(1i * out.varphiP1),  exp(-1i * out.varphiP1), ...
       -cot(out.thetaS1) * exp(1i * out.varphiS1), ...
        cot(out.thetaS1) * exp(-1i * out.varphiS1); ...
        cot(out.thetaP1) * exp(1i * out.varphiP1), ...
       -cot(out.thetaP1) * exp(-1i * out.varphiP1), ...
        exp(1i * out.varphiS1), exp(-1i * out.varphiS1); ...
        p.rho_1 * out.zeta_1 * sin(2 * out.thetaP1) * exp(1i * out.varphiP1), ...
       -p.rho_1 * out.zeta_1 * sin(2 * out.thetaP1) * exp(-1i * out.varphiP1), ...
       -p.rho_1 * cos(2 * out.thetaS1) * exp(1i * out.varphiS1), ...
       -p.rho_1 * cos(2 * out.thetaS1) * exp(-1i * out.varphiS1); ...
        p.rho_1 * cos(2 * out.thetaS1) * exp(1i * out.varphiP1), ...
        p.rho_1 * cos(2 * out.thetaS1) * exp(-1i * out.varphiP1), ...
        p.rho_1 * sin(2 * out.thetaS1) * exp(1i * out.varphiS1), ...
       -p.rho_1 * sin(2 * out.thetaS1) * exp(-1i * out.varphiS1)];

    out.P1 = A0 / Aphi;

    % ----------- common coefficient columns -----------
    coeff1 = [ ...
       -1; ...
        cot(out.thetaPa); ...
        p.rho_a * out.zeta_a * sin(2 * out.thetaPa); ...
       -p.rho_a * cos(2 * out.thetaSa)];

    coeff2 = [ ...
       -cot(out.thetaSa); ...
       -1; ...
        p.rho_a * cos(2 * out.thetaSa); ...
        p.rho_a * sin(2 * out.thetaSa)];

    coeff3 = out.P1 * [ ...
        1; ...
        cot(out.thetaPg); ...
        p.rho_g * out.zeta_g * sin(2 * out.thetaPg); ...
        p.rho_g * cos(2 * out.thetaSg)];

    coeff4 = out.P1 * [ ...
       -cot(out.thetaSg); ...
        1; ...
       -p.rho_g * cos(2 * out.thetaSg); ...
        p.rho_g * sin(2 * out.thetaSg)];

    A = [coeff1, coeff2, coeff3, coeff4];

    % ----------- P incidence -----------
    rhsP = [ ...
        1; ...
        cot(out.thetaPa); ...
        p.rho_a * out.zeta_a * sin(2 * out.thetaPa); ...
        p.rho_a * cos(2 * out.thetaSa)] * p.Phi_i;

    solP = A \ rhsP;
    out.phi_r_Pinc = solP(1);
    out.psi_r_Pinc = solP(2);
    out.phi_t_Pinc = solP(3);
    out.psi_t_Pinc = solP(4);

    out.rP_P  = out.phi_r_Pinc / p.Phi_i;
    out.rSV_P = out.psi_r_Pinc / p.Phi_i;
    out.tP_P  = out.phi_t_Pinc / p.Phi_i;
    out.tSV_P = out.psi_t_Pinc / p.Phi_i;

    out.RP_P  = abs(out.rP_P)^2;
    out.RSV_P = (out.cPa * cos(out.thetaSa)) / (out.cSa * cos(out.thetaPa)) * abs(out.rSV_P)^2;
    out.TP_P  = (out.eta_g * out.cPa * cos(out.thetaPg)) / (out.eta_a * out.cPg * cos(out.thetaPa)) * abs(out.tP_P)^2;
    out.TSV_P = (out.eta_g * out.cPa * cos(out.thetaSg)) / (out.eta_a * out.cSg * cos(out.thetaPa)) * abs(out.tSV_P)^2;
    out.EP    = out.RP_P + out.RSV_P + out.TP_P + out.TSV_P;

    % ----------- SV incidence -----------
    rhsSV = [ ...
       -cot(out.thetaSa); ...
        1; ...
       -p.rho_a * cos(2 * out.thetaSa); ...
        p.rho_a * sin(2 * out.thetaSa)] * p.Psi_i;

    solSV = A \ rhsSV;
    out.phi_r_SVinc = solSV(1);
    out.psi_r_SVinc = solSV(2);
    out.phi_t_SVinc = solSV(3);
    out.psi_t_SVinc = solSV(4);

    out.rP_SV  = out.phi_r_SVinc / p.Psi_i;
    out.rSV_SV = out.psi_r_SVinc / p.Psi_i;
    out.tP_SV  = out.phi_t_SVinc / p.Psi_i;
    out.tSV_SV = out.psi_t_SVinc / p.Psi_i;

    out.RP_SV  = (out.cSa * cos(out.thetaPa)) / (out.cPa * cos(out.thetaSa)) * abs(out.rP_SV)^2;
    out.RSV_SV = abs(out.rSV_SV)^2;
    out.TP_SV  = (out.eta_g * out.cSa * cos(out.thetaPg)) / (out.eta_a * out.cPg * cos(out.thetaSa)) * abs(out.tP_SV)^2;
    out.TSV_SV = (out.eta_g * out.cSa * cos(out.thetaSg)) / (out.eta_a * out.cSg * cos(out.thetaSa)) * abs(out.tSV_SV)^2;
    out.ESV    = out.RP_SV + out.RSV_SV + out.TP_SV + out.TSV_SV;

    % ----------- SH incidence -----------
    denSH = ...
        out.zeta_a * cos(out.thetaSa) * ...
        (cos(out.varphiS1) ...
        - 1i * (1 / out.zeta_1) * sin(out.varphiS1) / cos(out.thetaS1) ...
        * out.zeta_g * cos(out.thetaSg)) ...
        + ( ...
        -1i * out.zeta_1 * sin(out.varphiS1) * cos(out.thetaS1) ...
        + cos(out.varphiS1) * out.zeta_g * cos(out.thetaSg));

    numSH = ...
        out.zeta_a * cos(out.thetaSa) * ...
        (cos(out.varphiS1) ...
        - 1i * (1 / out.zeta_1) * sin(out.varphiS1) / cos(out.thetaS1) ...
        * out.zeta_g * cos(out.thetaSg)) ...
        - ( ...
        -1i * out.zeta_1 * sin(out.varphiS1) * cos(out.thetaS1) ...
        + cos(out.varphiS1) * out.zeta_g * cos(out.thetaSg));

    out.rSH = numSH / denSH;
    out.RSH = abs(out.rSH)^2;

    out.tSH = (out.kSa / out.kSg) * (2 * out.zeta_a * cos(out.thetaSa)) / denSH;
    out.TSH = (out.zeta_g * cos(out.thetaSg)) / (out.zeta_a * cos(out.thetaSa)) * ...
              abs((out.kSg / out.kSa) * out.tSH)^2;

    out.ESH = out.RSH + out.TSH;

    % clean tiny imag parts
    fns = fieldnames(out);
    for i = 1:numel(fns)
        val = out.(fns{i});
        if isnumeric(val) && isscalar(val)
            out.(fns{i}) = realIfTiny(val);
        end
    end
end

function drawDerived(ax, p, out)
    prepAxes(ax);
    y = 0.98;
    putTitle('Example 1 / normalized input');
    putLatex(sprintf(['$\\lambda_a = %s,\\; \\mu_a = %s,\\; \\lambda_1 = %s,\\; \\mu_1 = %s$'], ...
        fmtTex(p.lambda_a), fmtTex(p.mu_a), fmtTex(p.lambda_1), fmtTex(p.mu_1)));
    putLatex(sprintf(['$\\lambda_g = %s,\\; \\mu_g = %s,\\; \\rho_a = %s,\\; \\rho_1 = %s,\\; \\rho_g = %s$'], ...
        fmtTex(p.lambda_g), fmtTex(p.mu_g), fmtTex(p.rho_a), fmtTex(p.rho_1), fmtTex(p.rho_g)));
    putLatex(sprintf('$k_x = %s,\\quad h_1 = %s,\\quad \\omega = %s$', ...
        fmtTex(p.k_x), fmtTex(p.h_1), fmtTex(p.omega)));

    putTitle('Derived quantities');
    putLatex(sprintf('$k_{Pa}=%s,\\; k_{Sa}=%s,\\; k_{P1}=%s,\\; k_{S1}=%s,\\; k_{Pg}=%s,\\; k_{Sg}=%s$', ...
        fmtTex(out.kPa), fmtTex(out.kSa), fmtTex(out.kP1), fmtTex(out.kS1), fmtTex(out.kPg), fmtTex(out.kSg)));
    putLatex(sprintf('$c_{Pa}=%s,\\; c_{Sa}=%s,\\; c_{Pg}=%s,\\; c_{Sg}=%s$', ...
        fmtTex(out.cPa), fmtTex(out.cSa), fmtTex(out.cPg), fmtTex(out.cSg)));
    putLatex(sprintf('$\\zeta_a=%s,\\; \\zeta_1=%s,\\; \\zeta_g=%s$', ...
        fmtTex(out.zeta_a), fmtTex(out.zeta_1), fmtTex(out.zeta_g)));
    putLatex(sprintf('$\\theta_{Pa}=%s,\\; \\theta_{Sa}=%s,\\; \\theta_{P1}=%s,\\; \\theta_{S1}=%s$', ...
        fmtTex(out.thetaPa), fmtTex(out.thetaSa), fmtTex(out.thetaP1), fmtTex(out.thetaS1)));
    putLatex(sprintf('$\\theta_{Pg}=%s,\\; \\theta_{Sg}=%s$', ...
        fmtTex(out.thetaPg), fmtTex(out.thetaSg)));
    putLatex(sprintf('$\\varphi_{P1}=%s,\\; \\varphi_{S1}=%s$', ...
        fmtTex(out.varphiP1), fmtTex(out.varphiS1)));

    function putTitle(str)
        text(ax, 0.01, y, str, 'Interpreter', 'none', 'FontWeight', 'bold', ...
            'FontSize', 12, 'VerticalAlignment', 'top');
        y = y - 0.07;
    end
    function putLatex(str)
        text(ax, 0.02, y, str, 'Interpreter', 'latex', ...
            'FontSize', 13, 'VerticalAlignment', 'top');
        y = y - 0.085;
    end
end

function drawP(ax, out)
    prepAxes(ax);
    y = 0.98;
    putTitle('P incidence');
    putLatex('$r_P = \phi_r/\phi_i,\quad R_P = |r_P|^2$');
    putLatex('$r_{SV} = \psi_r/\phi_i,\quad R_{SV} = \dfrac{c_{Pa}\cos\theta_{Sa}}{c_{Sa}\cos\theta_{Pa}}|r_{SV}|^2$');
    putLatex('$t_P = \phi_t/\phi_i,\quad T_P = \dfrac{\eta_g c_{Pa}\cos\theta_{Pg}}{\eta_a c_{Pg}\cos\theta_{Pa}}|t_P|^2$');
    putLatex('$t_{SV} = \psi_t/\phi_i,\quad T_{SV} = \dfrac{\eta_g c_{Pa}\cos\theta_{Sg}}{\eta_a c_{Sg}\cos\theta_{Pa}}|t_{SV}|^2$');

    putTitle('Numerical results');
    putLatex(sprintf('$r_P = %s,\qquad R_P = %s$', fmtTex(out.rP_P), fmtTex(out.RP_P)));
    putLatex(sprintf('$r_{SV} = %s,\qquad R_{SV} = %s$', fmtTex(out.rSV_P), fmtTex(out.RSV_P)));
    putLatex(sprintf('$t_P = %s,\qquad T_P = %s$', fmtTex(out.tP_P), fmtTex(out.TP_P)));
    putLatex(sprintf('$t_{SV} = %s,\qquad T_{SV} = %s$', fmtTex(out.tSV_P), fmtTex(out.TSV_P)));
    putLatex(sprintf('$R_P + R_{SV} + T_P + T_{SV} = %s$', fmtTex(out.EP)));

    function putTitle(str)
        text(ax, 0.01, y, str, 'Interpreter', 'none', 'FontWeight', 'bold', ...
            'FontSize', 12, 'VerticalAlignment', 'top');
        y = y - 0.07;
    end
    function putLatex(str)
        text(ax, 0.02, y, str, 'Interpreter', 'latex', ...
            'FontSize', 13, 'VerticalAlignment', 'top');
        y = y - 0.085;
    end
end

function drawSV(ax, out)
    prepAxes(ax);
    y = 0.98;
    putTitle('SV incidence');
    putLatex('$r_P = \phi_r/\psi_i,\quad R_P = \dfrac{c_{Sa}\cos\theta_{Pa}}{c_{Pa}\cos\theta_{Sa}}|r_P|^2$');
    putLatex('$r_{SV} = \psi_r/\psi_i,\quad R_{SV} = |r_{SV}|^2$');
    putLatex('$t_P = \phi_t/\psi_i,\quad T_P = \dfrac{\eta_g c_{Sa}\cos\theta_{Pg}}{\eta_a c_{Pg}\cos\theta_{Sa}}|t_P|^2$');
    putLatex('$t_{SV} = \psi_t/\psi_i,\quad T_{SV} = \dfrac{\eta_g c_{Sa}\cos\theta_{Sg}}{\eta_a c_{Sg}\cos\theta_{Sa}}|t_{SV}|^2$');

    putTitle('Numerical results');
    putLatex(sprintf('$r_P = %s,\qquad R_P = %s$', fmtTex(out.rP_SV), fmtTex(out.RP_SV)));
    putLatex(sprintf('$r_{SV} = %s,\qquad R_{SV} = %s$', fmtTex(out.rSV_SV), fmtTex(out.RSV_SV)));
    putLatex(sprintf('$t_P = %s,\qquad T_P = %s$', fmtTex(out.tP_SV), fmtTex(out.TP_SV)));
    putLatex(sprintf('$t_{SV} = %s,\qquad T_{SV} = %s$', fmtTex(out.tSV_SV), fmtTex(out.TSV_SV)));
    putLatex(sprintf('$R_P + R_{SV} + T_P + T_{SV} = %s$', fmtTex(out.ESV)));

    function putTitle(str)
        text(ax, 0.01, y, str, 'Interpreter', 'none', 'FontWeight', 'bold', ...
            'FontSize', 12, 'VerticalAlignment', 'top');
        y = y - 0.07;
    end
    function putLatex(str)
        text(ax, 0.02, y, str, 'Interpreter', 'latex', ...
            'FontSize', 13, 'VerticalAlignment', 'top');
        y = y - 0.085;
    end
end

function drawSH(ax, out)
    prepAxes(ax);
    y = 0.98;
    putTitle('SH incidence');
    putLatex('$r_{SH} = \psi_r/\psi_i,\quad R_{SH} = |r_{SH}|^2$');
    putLatex('$t_{SH} = \psi_t/\psi_i,\quad T_{SH} = \dfrac{\zeta_g \cos\theta_{Sg}}{\zeta_a \cos\theta_{Sa}}\left|\dfrac{k_{Sg}}{k_{Sa}}t_{SH}\right|^2$');

    putTitle('Numerical results');
    putLatex(sprintf('$r_{SH} = %s,\qquad R_{SH} = %s$', fmtTex(out.rSH), fmtTex(out.RSH)));
    putLatex(sprintf('$t_{SH} = %s,\qquad T_{SH} = %s$', fmtTex(out.tSH), fmtTex(out.TSH)));
    putLatex(sprintf('$R_{SH} + T_{SH} = %s$', fmtTex(out.ESH)));

    function putTitle(str)
        text(ax, 0.01, y, str, 'Interpreter', 'none', 'FontWeight', 'bold', ...
            'FontSize', 12, 'VerticalAlignment', 'top');
        y = y - 0.07;
    end
    function putLatex(str)
        text(ax, 0.02, y, str, 'Interpreter', 'latex', ...
            'FontSize', 13, 'VerticalAlignment', 'top');
        y = y - 0.10;
    end
end

function drawEnergy(ax, out)
    prepAxes(ax);
    y = 0.98;
    putTitle('Energy conservation');
    putLatex(sprintf('$E_P = R_P + R_{SV} + T_P + T_{SV} = %s$', fmtTex(out.EP)));
    putLatex(sprintf('$E_{SV} = R_P + R_{SV} + T_P + T_{SV} = %s$', fmtTex(out.ESV)));
    putLatex(sprintf('$E_{SH} = R_{SH} + T_{SH} = %s$', fmtTex(out.ESH)));

    putTitle('Compact summary');
    putLatex(sprintf('$\\mathrm{P:}\\quad r_P=%s,\\; R_P=%s,\\; r_{SV}=%s,\\; R_{SV}=%s$', ...
        fmtTex(out.rP_P), fmtTex(out.RP_P), fmtTex(out.rSV_P), fmtTex(out.RSV_P)));
    putLatex(sprintf('$\\qquad t_P=%s,\\; T_P=%s,\\; t_{SV}=%s,\\; T_{SV}=%s$', ...
        fmtTex(out.tP_P), fmtTex(out.TP_P), fmtTex(out.tSV_P), fmtTex(out.TSV_P)));

    putLatex(sprintf('$\\mathrm{SV:}\\quad r_P=%s,\\; R_P=%s,\\; r_{SV}=%s,\\; R_{SV}=%s$', ...
        fmtTex(out.rP_SV), fmtTex(out.RP_SV), fmtTex(out.rSV_SV), fmtTex(out.RSV_SV)));
    putLatex(sprintf('$\\qquad t_P=%s,\\; T_P=%s,\\; t_{SV}=%s,\\; T_{SV}=%s$', ...
        fmtTex(out.tP_SV), fmtTex(out.TP_SV), fmtTex(out.tSV_SV), fmtTex(out.TSV_SV)));

    putLatex(sprintf('$\\mathrm{SH:}\\quad r_{SH}=%s,\\; R_{SH}=%s,\\; t_{SH}=%s,\\; T_{SH}=%s$', ...
        fmtTex(out.rSH), fmtTex(out.RSH), fmtTex(out.tSH), fmtTex(out.TSH)));

    function putTitle(str)
        text(ax, 0.01, y, str, 'Interpreter', 'none', 'FontWeight', 'bold', ...
            'FontSize', 12, 'VerticalAlignment', 'top');
        y = y - 0.07;
    end
    function putLatex(str)
        text(ax, 0.02, y, str, 'Interpreter', 'latex', ...
            'FontSize', 13, 'VerticalAlignment', 'top');
        y = y - 0.085;
    end
end

function drawError(ax, msg)
    prepAxes(ax);
    text(ax, 0.02, 0.95, 'Calculation failed:', ...
        'Interpreter', 'none', ...
        'Color', [0.75 0 0], ...
        'FontWeight', 'bold', ...
        'FontSize', 12, ...
        'VerticalAlignment', 'top');
    text(ax, 0.02, 0.86, msg, ...
        'Interpreter', 'none', ...
        'Color', [0.75 0 0], ...
        'FontSize', 11, ...
        'VerticalAlignment', 'top');
end

function prepAxes(ax)
    cla(ax);
    axis(ax, [0 1 0 1]);
    axis(ax, 'off');
    hold(ax, 'on');
end

function z = realIfTiny(z)
    if ~isnumeric(z) || ~isscalar(z)
        return;
    end
    tol = 1e-11 * max(1, abs(real(z)));
    if abs(imag(z)) < tol
        z = real(z);
    end
end

function s = fmtTex(x)
    x = realIfTiny(x);

    if isnan(x)
        s = '\mathrm{NaN}';
        return;
    end

    if isinf(x)
        if x > 0
            s = '\infty';
        else
            s = '-\infty';
        end
        return;
    end

    if isreal(x)
        s = sprintf('%.6g', x);
        return;
    end

    re = real(x);
    imv = imag(x);

    if abs(re) < 1e-14
        re = 0;
    end
    if abs(imv) < 1e-14
        imv = 0;
    end

    if re == 0
        if imv >= 0
            s = sprintf('%.6g\\mathrm{i}', imv);
        else
            s = sprintf('-%.6g\\mathrm{i}', abs(imv));
        end
    else
        if imv >= 0
            s = sprintf('%.6g + %.6g\\mathrm{i}', re, abs(imv));
        else
            s = sprintf('%.6g - %.6g\\mathrm{i}', re, abs(imv));
        end
    end
end
