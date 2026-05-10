if graphics_3D:
    betas      = [0.01, 0.05, 0.1]
    N_range    = range(100, 1000, 50)
    K_range    = [4, 5, 6, 7, 8, 9, 10]

    good_data, results = search_parameters(betas, N_range, K_range)

    if do_plot:
        plot_3d_surface(results)

    print_good_data(good_data)
